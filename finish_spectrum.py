from pyui.finish_spectrum import Ui_FinishSpectrum
from PyQt5.QtWidgets import QWidget, QToolBar, QDialog, QDialogButtonBox, QFileDialog, QMenu, QAction, QInputDialog, QVBoxLayout, QLineEdit, QTextEdit, QSpinBox, QLabel
from qmathplotwidget import QMathPlotWidget
from fits_spectrum import FitsSpectrum, Spectrum
from qtcommons import *
from astropy.io import fits
from scipy.interpolate import *
from reference_spectra_dialog import ReferenceSpectraDialog
from lines_dialog import LinesDialog
from matplotlib.lines import Line2D
from pyspectrum_commons import *
from reference_line import ReferenceLine
from matplotlib import gridspec
import matplotlib as plt
import numpy as np
import math
from view_object_properties import ViewObjectProperties, ObjectProperties
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from moveable_label import MoveableLabel
from lambda2color import *
from concurrent.futures import ThreadPoolExecutor

class FinishSpectrum(QWidget):
    def __init__(self, fits_file, settings, database):
        super(FinishSpectrum, self).__init__()
        self.settings = settings
        self.ui = Ui_FinishSpectrum()
        self.ui.setupUi(self)
        self.profile_line = None
        self.fits_spectrum = FitsSpectrum(fits_file)
        self.fits_spectrum.spectrum.normalize_to_max()
        self.spectrum = self.fits_spectrum.spectrum
        self.spectrum_plot = QtCommons.nestWidget(self.ui.plot, QMathPlotWidget())
        self.split_view()
        self.toolbar = QToolBar('Finish Spectrum Toolbar')
        self.toolbar.addAction('Instrument Response', lambda: QtCommons.open_file('Open Instrument Response Profile', FITS_EXTS, lambda f: self.instrument_response(f[0])))
        self.toolbar.addAction("Zoom", lambda: self.spectrum_plot.select_zoom(self.profile_plot.axes))
        self.toolbar.addAction("Reset Zoom", lambda: self.spectrum_plot.reset_zoom(self.spectrum.wavelengths, self.spectrum.fluxes.min(), self.spectrum.fluxes.max(), self.profile_plot.axes))
        remove_action = QtCommons.addToolbarPopup(self.toolbar, "Remove")
        remove_action.menu().addAction("Before point", lambda: spectrum_trim_dialog(self.spectrum, 'before', self.profile_plot.axes, lambda: self.draw()))
        remove_action.menu().addAction("After point", lambda: spectrum_trim_dialog(self.spectrum, 'after', self.profile_plot.axes, lambda: self.draw()))
        self.toolbar.addSeparator()
        
        self.reference_spectra_dialog = ReferenceSpectraDialog(database)
        self.reference_spectra_dialog.setup_menu(self.toolbar, self.profile_plot.axes)
        
        lines_menu = QtCommons.addToolbarPopup(self.toolbar, "Spectral Lines...")
        lines_menu.menu().addAction('Lines Database', lambda: self.lines_dialog.show())
        lines_menu.menu().addAction('Custom line', self.add_custom_line)
        
        self.toolbar.addSeparator()
        self.object_properties_dialog = ViewObjectProperties.dialog(fits_file)
        self.toolbar.addAction("Properties", self.object_properties_dialog.show)
        self.toolbar.addSeparator()
        self.toolbar.addAction("Export Image...", lambda: QtCommons.save_file('Export plot to image', 'PNG (*.png);;PDF (*.pdf);;PostScript (*.ps);;SVG (*.svg)', lambda f: self.save_image(f[0]), self.settings.value('last_save_image_dir')))
        self.lines_dialog = LinesDialog(database, settings, self.spectrum_plot, self.profile_plot.axes)
        self.lines_dialog.lines.connect(self.add_lines)
        save_action = self.toolbar.addAction(QIcon.fromTheme('document-save'), 'Save', lambda: QtCommons.save_file('Save plot...', 'FITS file (.fit)', self.save, self.settings.value('last_save_finished_dir')))
        
        self.add_info(fits_file)
        
        self.lines = []
        hdu_spectral_lines = [h for h in fits_file if h.name == FitsSpectrum.SPECTRAL_LINES]
        if len(hdu_spectral_lines) > 0:                
            for line in hdu_spectral_lines[-1].data:
                try:
                    text = line[0].decode()
                except AttributeError:
                    print("Warning: Attribute error on decode")
                    text = line[0]
                self.lines.append(ReferenceLine(text, line[1], self.profile_plot.axes, lambda line: self.lines.remove(line), show_wavelength=line[3], fontsize=line[2], position=(line[4], line[5])))
                
    
        
    def add_custom_line(self):
        wl = QInputDialog.getDouble(self, "Custom Line", "Enter line wavelength in Å", self.fits_spectrum.spectrum.wavelengths[0],self.fits_spectrum.spectrum.wavelengths[0],self.fits_spectrum.spectrum.wavelengths[-1],3)
        if not wl[1]: return
        self.add_lines([{'name': 'Custom Line', 'lambda': wl[0]}])
        
    def add_lines(self, lines):
        for line in lines:
            self.lines.append(ReferenceLine(line['name'], line['lambda'], self.profile_plot.axes, lambda line: self.lines.remove(line)))

    def synthetize(wavelength, flux):
        crange = (3800, 7800)
        if not crange[0] < wavelength < crange[1]: return (0,0,0,0)
        value = plt.cm.gist_rainbow(1-((wavelength-crange[0]) / (crange[1]-crange[0]) ) )
        return [value[0], value[1], value[2], math.pow(flux, 3/5)]
    
    def synthetize_img(wavelengths, fluxes):
        f_fluxes = lambda f: math.pow(f, 3/5)
        colors = [wavelength_to_rgb(w/10., f_fluxes(fluxes[i])) for i,w in enumerate(wavelengths)]
        im_height = 150
        colors = np.array(colors*im_height).reshape(im_height,len(colors),4)
        return colors, im_height
        

    def split_view(self):
        figure = self.spectrum_plot.figure
        figure.clear()
        self.gs = gridspec.GridSpec(40,1)
        self.profile_plot = figure.add_subplot(self.gs[0:-6])
        self.synthetize = figure.add_subplot(self.gs[-3:-1], sharex = self.profile_plot)
        self.synthetize.yaxis.set_visible(False)
        self.synthetize.xaxis.set_visible(False)
        self.draw()
        
    
    def draw(self):
#        self.profile_plot.clear()
        if self.profile_line:
            self.profile_line.remove()
        self.profile_line = self.profile_plot.plot(self.spectrum.wavelengths, self.spectrum.fluxes, color='blue')[0]

        self.synthetize.axes.set_axis_bgcolor('black')
        
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(FinishSpectrum.synthetize_img, self.spectrum.wavelengths, self.spectrum.fluxes)
            future.add_done_callback(lambda f: self.synthetize.imshow(f.result()[0], extent=[self.spectrum.wavelengths[0], self.spectrum.wavelengths[-1], 0, f.result()[1]]) )

        self.profile_plot.axes.set_xlabel('wavelength (Å)')
        self.profile_plot.axes.set_ylabel('relative flux')
        self.profile_plot.axes.xaxis.set_major_locator(MultipleLocator(200))
        self.profile_plot.axes.xaxis.set_minor_locator(MultipleLocator(20))
        self.spectrum_plot.figure.canvas.draw()
        self.gs.tight_layout(self.spectrum_plot.figure)
        
    def instrument_response(self, filename):
        instrument_response_file = fits.open(filename)
        instrument_response = FitsSpectrum(instrument_response_file)
        response = instrument_response.spectrum
        response.normalize_to_max()
        
        range = (max(response.wavelengths[0], self.spectrum.wavelengths[0] ), min(response.wavelengths[-1], self.spectrum.wavelengths[-1]))
        self.spectrum.cut(self.spectrum.wavelength_index(range[0]), self.spectrum.wavelength_index(range[1]))
        spline = InterpolatedUnivariateSpline(response.wavelengths, response.fluxes)
        
        response_data = [spline(x) for x in self.spectrum.wavelengths]
        self.spectrum.fluxes /= response_data
        self.spectrum.normalize_to_max()
        self.draw()
        
        
    def save_image(self, filename):
        self.settings.setValue('last_save_image_dir', os.path.dirname(filename))
        self.spectrum_plot.figure.savefig(filename, bbox_inches='tight', dpi=300)

    def save(self, filename):
        filename = filename[0]
        self.settings.setValue('last_save_finished_dir', os.path.dirname(filename))
        self.fits_spectrum.save(filename, spectral_lines = self.lines)
        
        
    def add_info(self, fits_file):
        properties = ObjectProperties(fits_file)
        info_text = "Object Name: {}, type: {}, spectral class: {}\nCoordinates: {}\nDate: {}\nObserver: {}\nEquipment: {}\nPosition: {}".format(
                properties.name,
                properties.type,
                properties.sptype,
                properties.printable_coordinates(),
                properties.date.toString(),
                properties.observer,
                properties.equipment,
                properties.position
            )
        self.title_widget = MoveableLabel(text=properties.name, on_dblclick=lambda: self.edit_label(self.title_widget), x=self.spectrum.wavelengths[len(self.spectrum.wavelengths)/2-100], y=0.95, fontsize=25, color='black', axes=self.profile_plot.axes)
        self.info_widget = MoveableLabel(text=info_text, on_dblclick=lambda: self.edit_label(self.info_widget, type='textbox'), x=self.spectrum.wavelengths[len(self.spectrum.wavelengths)/4*3], y=0.80, fontsize=14, color='black', axes=self.profile_plot.axes)

    def edit_label(self, label, type='lineedit'):
        dialog = QDialog()
        dialog.setWindowTitle("Edit Label")
        dialog.setLayout(QVBoxLayout())
        font_size = QSpinBox()
        font_size.setValue(label.get_fontsize())
        dialog.layout().addWidget(QLabel("Font Size"))
        dialog.layout().addWidget(font_size)
        text_edit = None
        if type == 'lineedit':
            text_edit = QLineEdit(label.get_text())
        else:
            text_edit = QTextEdit()
            text_edit.setPlainText(label.get_text())
            
        dialog.layout().addWidget(QLabel("Text"))
        dialog.layout().addWidget(text_edit)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        dialog.layout().addWidget(button_box)
        if QDialog.Accepted != dialog.exec():
            return
        label.set_text(text_edit.text() if type=='lineedit' else text_edit.toPlainText())
        label.set_fontsize(font_size.value())
        label.axes.figure.canvas.draw()