from ui_finish_spectrum import Ui_FinishSpectrum
from PyQt5.QtWidgets import QWidget, QToolBar, QDialog, QDialogButtonBox, QFileDialog, QMenu, QAction, QInputDialog
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

class FinishSpectrum(QWidget):
    def __init__(self, fits_file, settings, database):
        super(FinishSpectrum, self).__init__()
        self.settings = settings
        self.ui = Ui_FinishSpectrum()
        self.ui.setupUi(self)
        self.fits_spectrum = FitsSpectrum(fits_file)
        self.fits_spectrum.spectrum.normalize_to_max()
        self.spectrum = self.fits_spectrum.spectrum
        self.spectrum_plot = QtCommons.nestWidget(self.ui.plot, QMathPlotWidget())
        self.toolbar = QToolBar('Finish Spectrum Toolbar')
        self.toolbar.addAction('Instrument Response', lambda: QtCommons.open_file('Open Instrument Response Profile', FITS_EXTS, lambda f: self.instrument_response(f[0])))
        self.toolbar.addAction("Zoom", lambda: self.spectrum_plot.select_zoom(self.profile_plot.axes))
        self.toolbar.addAction("Reset Zoom", lambda: self.spectrum_plot.reset_zoom(self.spectrum.wavelengths, self.spectrum.fluxes.min(), self.spectrum.fluxes.max(), self.profile_plot.axes))
        remove_action = QtCommons.addToolbarPopup(self.toolbar, "Remove")
        remove_action.menu().addAction("Before point", lambda: self.remove('before'))
        remove_action.menu().addAction("After point", lambda: self.remove('after'))
        self.toolbar.addSeparator()
        self.reference_spectra_dialog = ReferenceSpectraDialog(database)
        self.reference_spectra_dialog.fits_picked.connect(self.open_reference)
        reference_action = QtCommons.addToolbarPopup(self.toolbar, "Reference")
        reference_action.menu().addAction("Load from FITS file", lambda: QtCommons.open_file('Open Reference Profile', FITS_EXTS, lambda f: self.open_reference(f[0])))
        reference_action.menu().addAction("Reference library", lambda: self.reference_spectra_dialog.show())
        reference_action.menu().addAction("Close", lambda: self.spectrum_plot.rm_element('reference'))
        
        lines_menu = QtCommons.addToolbarPopup(self.toolbar, "Spectral Lines...")
        lines_menu.menu().addAction('Lines Database', lambda: self.lines_dialog.show())
        lines_menu.menu().addAction('Custom line', self.add_custom_line)
        
        self.toolbar.addSeparator()
        self.toolbar.addAction("Export Image...", lambda: QtCommons.save_file('Export plot to image', 'PNG (*.png);;PDF (*.pdf);;PostScript (*.ps);;SVG (*.svg)', lambda f: self.spectrum_plot.figure.savefig(f[0], bbox_inches='tight', dpi=300)))
        self.split_view()
        self.draw()
        self.lines_dialog = LinesDialog(database, settings, self.spectrum_plot, self.profile_plot.axes)
        self.lines_dialog.lines.connect(self.add_lines)
        save_action = self.toolbar.addAction(QIcon.fromTheme('document-save'), 'Save', lambda: QtCommons.save_file('Save plot...', 'FITS file (.fit)', self.save, self.settings.value('last_save_plot_dir')))
        self.lines = []
        
    def add_custom_line(self):
        wl = QInputDialog.getDouble(self, "Custom Line", "Enter line wavelength in Å", self.fits_spectrum.spectrum.wavelengths[0],self.fits_spectrum.spectrum.wavelengths[0],self.fits_spectrum.spectrum.wavelengths[-1],3)
        if not wl[1]: return
        self.add_lines([{'name': 'Custom Line', 'lambda': wl[0]}])
        
    def add_lines(self, lines):
        for line in lines:
            self.lines.append(ReferenceLine(line['name'], line['lambda'], self.profile_plot.axes, lambda line: self.lines.remove(line)))
        
    def split_view(self):
        figure = self.spectrum_plot.figure
        figure.clear()
        gs = gridspec.GridSpec(11,1)
        self.profile_plot = figure.add_subplot(gs[0:-1])
        self.synthetize = figure.add_subplot(gs[-1], sharex = self.profile_plot)
        self.synthetize.yaxis.set_visible(False)
        self.synthetize.xaxis.set_visible(False)
        self.draw()
        
    def synthetize(wavelength, flux):
        crange = (3800, 7800)
        if not crange[0] < wavelength < crange[1]: return (0,0,0,0)
        value = plt.cm.gist_rainbow(1-((wavelength-crange[0]) / (crange[1]-crange[0]) ) )
        return [value[0], value[1], value[2], math.sqrt(flux)]
    
    def draw(self):
        self.profile_plot.clear()
        self.profile_plot.plot(self.spectrum.wavelengths, self.spectrum.fluxes)

        self.synthetize.axes.set_axis_bgcolor('black')
        colors = [FinishSpectrum.synthetize(w, self.spectrum.fluxes[i]) for i,w in enumerate(self.spectrum.wavelengths)]
        im_height = 100
        colors = np.array(colors*im_height).reshape(im_height,len(colors),4)
        self.synthetize.imshow(colors, extent=[self.spectrum.wavelengths[0], self.spectrum.wavelengths[-1], 0, im_height])
        self.profile_plot.figure.tight_layout()
        self.profile_plot.axes.set_xlabel('lambda (Å)')
        self.profile_plot.axes.set_ylabel('relative flux')
        self.spectrum_plot.figure.canvas.draw()
        
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
        
    def remove(self, direction):
        point = QInputDialog.getInt(None, 'Trim curve', 'Enter wavelength for trimming', self.spectrum.wavelengths[0] if direction == 'before' else self.spectrum.wavelengths[-1], self.spectrum.wavelengths[0], self.spectrum.wavelengths[-1])
        if not point[1]:
            return
        if direction == 'before':
            self.spectrum.cut(start=self.spectrum.wavelength_index(point[0]))
        else:
            self.spectrum.cut(end=self.spectrum.wavelength_index(point[0]))
            
        self.spectrum.normalize_to_max()
        self.draw()
        
    def open_reference(self, file):
        fits_spectrum = FitsSpectrum(fits.open(file))
        fits_spectrum.spectrum.normalize_to_max()
        line = Line2D(fits_spectrum.x_axis(), fits_spectrum.data(), color='gray')
        self.profile_plot.axes.add_line(line)
        self.spectrum_plot.add_element(line, 'reference')
        
    def save(self, filename):
        for line in self.lines:
            print(line)
        self.fits_spectrum.save(filename[0])
