from pyui.finish_spectrum import Ui_FinishSpectrum
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
from view_object_properties import ViewObjectProperties
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

import sys
import os
import traceback
import optparse
import time
import logging


#credits: http://www.noah.org/wiki/Wavelength_to_RGB_in_Python
def wavelength_to_rgb(wavelength, flux, gamma=0.8):

    '''This converts a given wavelength of light to an 
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''
    w=wavelength
    if w >= 380 and w < 440:
        R = -(w - 440.) / (440. - 380.)
        G = 0.0
        B = 1.0
    elif w >= 440 and w < 490:
        R = 0.0
        G = (w - 440.) / (490. - 440.)
        B = 1.0
    elif w >= 490 and w < 510:
        R = 0.0
        G = 1.0
        B = -(w - 510.) / (510. - 490.)
    elif w >= 510 and w < 580:
        R = (w - 510.) / (580. - 510.)
        G = 1.0
        B = 0.0
    elif w >= 580 and w < 645:
        R = 1.0
        G = -(w - 645.) / (645. - 580.)
        B = 0.0
    elif w >= 645 and w <= 780:
        R = 1.0
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return [R, G, B, flux]

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
        self.toolbar.addAction("Export Image...", lambda: QtCommons.save_file('Export plot to image', 'PNG (*.png);;PDF (*.pdf);;PostScript (*.ps);;SVG (*.svg)', lambda f: self.save_image(f[0])))
        self.lines_dialog = LinesDialog(database, settings, self.spectrum_plot, self.profile_plot.axes)
        self.lines_dialog.lines.connect(self.add_lines)
        save_action = self.toolbar.addAction(QIcon.fromTheme('document-save'), 'Save', lambda: QtCommons.save_file('Save plot...', 'FITS file (.fit)', self.save, self.settings.value('last_save_finished_dir')))
        
        self.draw()
        
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
        self.profile_plot.clear()

        self.profile_plot.plot(self.spectrum.wavelengths, self.spectrum.fluxes)

        self.synthetize.axes.set_axis_bgcolor('black')
        #colors = [FinishSpectrum.synthetize(w, self.spectrum.fluxes[i]) for i,w in enumerate(self.spectrum.wavelengths)]
        f_fluxes = lambda f: math.pow(f, 3/5)
        colors = [wavelength_to_rgb(w/10., f_fluxes(self.spectrum.fluxes[i])) for i,w in enumerate(self.spectrum.wavelengths)]
        im_height = 150
        colors = np.array(colors*im_height).reshape(im_height,len(colors),4)
        self.synthetize.imshow(colors, extent=[self.spectrum.wavelengths[0], self.spectrum.wavelengths[-1], 0, im_height])
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
