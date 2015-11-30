from ui_plots_math import Ui_PlotsMath
from scipy.interpolate import *
from qmathplotwidget import QMathPlotWidget
from PyQt5.QtWidgets import QWidget, QToolBar
from fits_spectrum import FitsSpectrum
from qtcommons import QtCommons
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QByteArray, QTimer
import numpy as np
from astropy.io import fits
from miles import Miles
from miles_dialog import MilesDialog

class PlotsMath(QWidget):
    def __init__(self, settings):
        super(PlotsMath, self).__init__()
        self.ui = Ui_PlotsMath()
        self.ui.setupUi(self)
        self.settings = settings
        self.plot = QtCommons.nestWidget(self.ui.plot, QMathPlotWidget())
        self.miles_dialog = MilesDialog()
        self.miles_dialog.fits_picked.connect(self.open_fits)
        self.toolbar = QToolBar('Instrument Response Toolbar')
        self.toolbar.addAction('Open', lambda: QtCommons.open_file('Open FITS Spectrum',"FITS Images (*.fit *.fits)", lambda f: self.open_fits(f[0]), self.settings.value("open_spectrum_last_dir", type=str) ))
        self.toolbar.addAction('MILES', self.miles_dialog.show)
        self.toolbar.addSeparator()
        self.toolbar.addAction('Zoom', self.start_zoom)
        self.toolbar.addAction('Reset Zoom', self.reset_zoom)
        self.ui.spline_factor.valueChanged.connect(self.factor_valueChanged)
        self.ui.spline_degrees.valueChanged.connect(lambda v: self.draw())
        self.ui.spline_factor_auto.toggled.connect(lambda v: self.draw())
        self.ui.spline_factor_auto.toggled.connect(lambda v: self.ui.spline_factor.setEnabled(not v))
        self.ui.remove_points.clicked.connect(self.pick_rm_points)
        
    def open_fits(self, filename):
        fits_file = fits.open(filename)
        self.fits_spectrum = FitsSpectrum(fits_file)
        self.x_axis = self.fits_spectrum.x_axis()
        self.data = self.fits_spectrum.data()
        self.draw()

    @pyqtSlot(float)
    def factor_valueChanged(self, f):
        self.draw()
        
    def pick_rm_points(self):
        self.plot.rm_element('zoom')
        self.plot.add_span_selector('pick_rm_points', lambda min,max: self.rm_points(min,max+1),direction='horizontal')
        
        
    def start_zoom(self):
        self.plot.rm_element('pick_rm_points')
        self.plot.add_rectangle_selector('zoom', self.zoom)
        
    def draw(self):
        self.ui.spline_degrees_value.setText("{}".format(self.ui.spline_degrees.value()))
        spline_factor = self.ui.spline_factor.value() if not self.ui.spline_factor_auto.isChecked() else None
        spline = UnivariateSpline(self.x_axis, self.data, k=self.ui.spline_degrees.value(), s=spline_factor)
        self.f_x = lambda x: spline[x]
        self.plot.axes.plot(self.x_axis, self.data, '--', self.x_axis, spline(self.x_axis), '-')
        self.plot.figure.canvas.draw()
        
    def rm_points(self, min, max):
        min = self.fits_spectrum.x_uncalibrated(min)
        max = self.fits_spectrum.x_uncalibrated(max)
        rect = lambda x: x*((self.data[max]-self.data[min])/(max-min)) + self.data[min]
        self.data[min:max] = np.fromfunction(rect, self.data[min:max].shape)
        self.draw()
        self.plot.rm_element('pick_rm_points')
        
    def zoom(self, a, b):
        self.plot.axes.axis([a.xdata, b.xdata, a.ydata, b.ydata])
        self.plot.rm_element('zoom')
        self.plot.figure.canvas.draw()
        
    def reset_zoom(self):
        self.plot.axes.axis([self.fits_spectrum.x_axis()[0], self.fits_spectrum.x_axis()[-1], self.fits_spectrum.data()[0], self.fits_spectrum.data()[-1]])
        self.draw()
        
    def save(self):
        pass
        