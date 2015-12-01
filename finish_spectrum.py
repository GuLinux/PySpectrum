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
        self.toolbar.addAction("Zoom", self.spectrum_plot.select_zoom)
        self.toolbar.addAction("Reset Zoom", lambda: self.spectrum_plot.reset_zoom(self.spectrum.wavelengths, self.spectrum.fluxes.min(), self.spectrum.fluxes.max()))
        remove_action = QtCommons.addToolbarPopup(self.toolbar, "Remove")
        remove_action.menu().addAction("Before point", lambda: self.remove('before'))
        remove_action.menu().addAction("After point", lambda: self.remove('after'))
        self.toolbar.addSeparator()
        self.reference_spectra_dialog = ReferenceSpectraDialog(database)
        self.reference_spectra_dialog.fits_picked.connect(self.open_reference)
        self.lines_dialog = LinesDialog()
        
        reference_action = QtCommons.addToolbarPopup(self.toolbar, "Reference")
        reference_action.menu().addAction("Load from FITS file", lambda: QtCommons.open_file('Open Reference Profile', FITS_EXTS, lambda f: self.open_reference(f[0])))
        reference_action.menu().addAction("Reference library", lambda: self.reference_spectra_dialog.show())
        reference_action.menu().addAction("Close", lambda: self.spectrum_plot.rm_element('reference'))
        
        self.toolbar.addAction('Spectral Lines', lambda: self.lines_dialog.show())
        
        self.toolbar.addSeparator()
        self.toolbar.addAction("Export Image...", lambda: QtCommons.save_file('Export plot to image', 'PNG (*.png);;PDF (*.pdf);;PostScript (*.ps);;SVG (*.svg)', lambda f: self.spectrum_plot.figure.savefig(f[0], bbox_inches='tight', dpi=300)))
        self.draw()
        save_action = self.toolbar.addAction(QIcon.fromTheme('document-save'), 'Save', lambda: QtCommons.save_file('Save plot...', 'FITS file (.fit)', self.save, self.settings.value('last_save_plot_dir')))
    def draw(self):
        self.spectrum_plot.plot(self.spectrum.wavelengths, self.spectrum.fluxes)
        self.spectrum_plot.axes.set_xlabel('lambda (Å)')
        self.spectrum_plot.axes.set_ylabel('relative flux')
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
        self.spectrum_plot.plot(self.spectrum.wavelengths, self.spectrum.fluxes, "-", self.spectrum.wavelengths, response_data, "--")
        
        
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
        self.spectrum_plot.axes.add_line(line)
        self.spectrum_plot.add_element(line, 'reference')
        
    def save(self, filename):
        self.fits_spectrum.save(filename[0])
