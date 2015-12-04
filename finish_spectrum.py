from pyui.finish_spectrum import Ui_FinishSpectrum
from PyQt5.QtWidgets import QWidget, QToolBar, QDialog, QDialogButtonBox, QFileDialog, QMenu, QAction, QInputDialog, QVBoxLayout, QLineEdit, QTextEdit, QSpinBox, QLabel, QPushButton
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
from object_properties import ObjectProperties
from object_properties_dialog import ObjectPropertiesDialog
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
        try:
            fits_file.index_of('ORIGINAL_DATA')
        except KeyError:
            hdu = fits.ImageHDU(data = fits_file[0].data, header = fits_file[0].header, name='ORIGINAL_DATA')
            fits_file.append(hdu)

        self.fits_spectrum.spectrum.normalize_to_max()
        self.spectrum = self.fits_spectrum.spectrum
        self.spectrum_plot = QtCommons.nestWidget(self.ui.plot, QMathPlotWidget())
        self.split_view()
        self.toolbar = QToolBar('Finish Spectrum Toolbar')
        self.toolbar.addAction('Instrument Response', lambda: open_file_sticky('Open Instrument Response Profile', FITS_EXTS, lambda f: self.instrument_response(f[0]), settings, MATH_OPERATION, [RAW_PROFILE]))
        self.toolbar.addAction("Zoom", lambda: self.spectrum_plot.select_zoom(self.profile_plot.axes))
        self.toolbar.addAction("Reset Zoom", lambda: self.spectrum_plot.reset_zoom(self.spectrum.wavelengths, self.spectrum.fluxes.min(), self.spectrum.fluxes.max(), self.profile_plot.axes))
        remove_action = QtCommons.addToolbarPopup(self.toolbar, "Remove")
        remove_action.menu().addAction("Before point", lambda: spectrum_trim_dialog(self.spectrum, 'before', self.profile_plot.axes, lambda: self.draw()))
        remove_action.menu().addAction("After point", lambda: spectrum_trim_dialog(self.spectrum, 'after', self.profile_plot.axes, lambda: self.draw()))
        self.toolbar.addSeparator()
        
        self.reference_spectra_dialog = ReferenceSpectraDialog(database)
        self.reference_spectra_dialog.setup_menu(self.toolbar, self.profile_plot.axes, settings)
        
        lines_menu = QtCommons.addToolbarPopup(self.toolbar, "Spectral Lines..")
        lines_menu.menu().addAction('Lines Database', lambda: self.lines_dialog.show())
        lines_menu.menu().addAction('Custom line', self.add_custom_line)
        labels_action = QtCommons.addToolbarPopup(self.toolbar, "Labels..")
        self.object_properties = ObjectProperties(fits_file)
        labels_action.menu().addAction('Title', self.add_title)
        if self.object_properties:
            labels_action.menu().addAction('Information from FITS file', self.add_fits_information_label)
        labels_action.menu().addAction('Custom', self.add_label)
        

        self.object_properties_dialog = ObjectPropertiesDialog(settings, self.object_properties)
        self.toolbar.addAction("Object properties", self.object_properties_dialog.show)

        self.labels, self.lines = [], []
        for label in self.fits_spectrum.labels():
            self.add_label(text=label['text'], coords=label['coords'], type=label['type'], fontsize=label['fontsize'])
        
        self.toolbar.addSeparator()
        self.toolbar.addAction(QIcon(':/image_20'), "Export Image...", lambda: save_file_sticky('Export plot to image', 'PNG (*.png);;PDF (*.pdf);;PostScript (*.ps);;SVG (*.svg)', lambda f: self.save_image(f[0]), self.settings, EXPORT_IMAGES, [CALIBRATED_PROFILE]))
        self.lines_dialog = LinesDialog(database, settings, self.spectrum_plot, self.profile_plot.axes)
        self.lines_dialog.lines.connect(self.add_lines)
        save_action = self.toolbar.addAction(QIcon(':/save_20'), 'Save', lambda: save_file_sticky('Save plot...', 'FITS file (.fit)', self.save, self.settings, CALIBRATED_PROFILE))
        for line in self.fits_spectrum.lines_labels():
            self.lines.append(ReferenceLine(line['text'], line['wavelength'], self.profile_plot.axes, lambda line: self.lines.remove(line), show_wavelength=line['display_wavelength'], fontsize=line['fontsize'], position=line['position']))
                
    
        
    def add_custom_line(self):
        wl = QInputDialog.getDouble(self, "Custom Line", "Enter line wavelength in Å", self.fits_spectrum.spectrum.wavelengths[0],self.fits_spectrum.spectrum.wavelengths[0],self.fits_spectrum.spectrum.wavelengths[-1],3)
        if not wl[1]: return
        self.add_lines([{'name': 'Custom Line', 'lambda': wl[0]}])
        
    def add_lines(self, lines):
        for line in lines:
            self.lines.append(ReferenceLine(line['name'], line['lambda'], self.profile_plot.axes, lambda line: self.lines.remove(line)))

    
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
        self.spectrum_plot.figure.savefig(filename, bbox_inches='tight', dpi=300)

    def save(self, filename):
        filename = filename[0]
        self.fits_spectrum.save(filename, spectral_lines = self.lines, labels = self.labels)
        
    def add_title(self):
        title = self.object_properties.name if self.object_properties else 'Title - double click to edit'
        self.add_label(text=title, coords=(self.spectrum.wavelengths[len(self.spectrum.wavelengths)/2-100], 0.95), fontsize=25, type='lineedit')
    
    def add_fits_information_label(self):
        info_text = "Object Name: {}, type: {}, spectral class: {}\nCoordinates: {}\nDate: {}\nObserver: {}\nEquipment: {}\nPosition: {}".format(
                self.object_properties.name,
                self.object_properties.type,
                self.object_properties.sptype,
                self.object_properties.printable_coordinates(),
                self.object_properties.date.toString(),
                self.object_properties.observer,
                self.object_properties.equipment,
                self.object_properties.position
            )
        self.add_label(info_text, type='textbox', coords=(self.spectrum.wavelengths[len(self.spectrum.wavelengths)/4*3], 0.80), fontsize=14)
        self.profile_plot.figure.canvas.draw()
    
    def add_label(self, text=None, type='textbox', coords = None, fontsize = 12, color='black'):
        if not coords: coords = (self.spectrum.wavelengths[len(self.spectrum.wavelengths)/2], 0.5)
        self.labels.append((type, MoveableLabel(text=text if text else 'Label - double click to edit', on_dblclick=lambda l: self.edit_label(l, type=type), x=coords[0], y=coords[1], fontsize=fontsize, color=color, axes=self.profile_plot.axes)))
        self.profile_plot.figure.canvas.draw()
        
    def edit_label(self, label, type='lineedit'):
        def remove_label(self, label, dialog):
            label.remove()
            self.labels.remove([l for l in self.labels if l[1] == label][0])
            self.profile_plot.figure.canvas.draw()
            dialog.reject()
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
        remove_button = QPushButton('Remove')
        remove_button.clicked.connect(lambda: remove_label(self, label, dialog))
        dialog.layout().addWidget(remove_button)
        dialog.layout().addWidget(button_box)
        if QDialog.Accepted != dialog.exec():
            return
        label.set_text(text_edit.text() if type=='lineedit' else text_edit.toPlainText())
        label.set_fontsize(font_size.value())
        label.axes.figure.canvas.draw()