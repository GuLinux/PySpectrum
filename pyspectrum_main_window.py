from ui_pyspectrum_main_window import Ui_PySpectrumMainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from import_image import ImportImage
from calibrate_spectrum import CalibrateSpectrum
from finish_spectrum import FinishSpectrum
from PyQt5.QtCore import QSettings, QByteArray
import os
from astropy.io import fits
from qtcommons import QtCommons
from plots_math import PlotsMath
from pyspectrum_commons import *
import sqlite3
from matplotlib import rc
from PyQt5.QtWidgets import QApplication

class PySpectrumMainWindow(QMainWindow):
    def __init__(self):
        font = QApplication.instance().font()
        rc('font', **{'family':'serif','serif':[font.defaultFamily()]})
        super(PySpectrumMainWindow, self).__init__()
        self.ui = Ui_PySpectrumMainWindow()
        self.database = sqlite3.connect('data/pyspectrum.db')
        self.ui.setupUi(self)
        self.settings = QSettings("GuLinux", "PySpectrum")
        QtCommons.addToolbarPopup(self.ui.toolBar, 'Load...', actions=[self.ui.actionOpen_Image,self.ui.actionCalibrate_FITS,self.ui.actionPlots_Math,self.ui.actionFinish_Spectrum])
        self.ui.actionOpen_Image.triggered.connect(lambda: QtCommons.open_file('Open FITS Image',FITS_IMG_EXTS, self.open_image, self.settings.value("open_image_last_dir", type=str) ))
        self.ui.actionCalibrate_FITS.triggered.connect(lambda: QtCommons.open_file('Open raw FITS Spectrum',FITS_EXTS, self.calibrate, self.settings.value("open_spectrum_last_dir", type=str) ))
        self.ui.actionPlots_Math.triggered.connect(self.plots_math)
        self.ui.actionFinish_Spectrum.triggered.connect(lambda: QtCommons.open_file('Open FITS Spectrum',FITS_EXTS, self.finish_spectrum, self.settings.value("open_spectrum_last_dir", type=str) ))
        self.ui.stackedWidget.currentChanged.connect(self.current_changed)
        self.current_widget_toolbar = None
        self.restoreGeometry(self.settings.value('window_geometry', QByteArray()))
        
    def closeEvent(self, ev):
        self.settings.setValue('window_geometry', self.saveGeometry())
        QMainWindow.closeEvent(self, ev)
        
    def current_changed(self, index):
        if self.current_widget_toolbar:
            self.removeToolBar(self.current_widget_toolbar)
        self.current_widget_toolbar = self.ui.stackedWidget.currentWidget().toolbar
        self.addToolBar(self.current_widget_toolbar)
        
    def open_image(self, file):
        fits_file = self.open_fits(file[0], "open_image")
        self.import_image = ImportImage(fits_file, self.settings)
        self.ui.stackedWidget.addWidget(self.import_image)
        self.ui.stackedWidget.setCurrentWidget(self.import_image)
    
    def calibrate(self, file):
        fits_file = self.open_fits(file[0], 'open_spectrum')
        widget = CalibrateSpectrum(fits_file, self.settings, self.database)
        self.ui.stackedWidget.addWidget(widget)
        self.ui.stackedWidget.setCurrentWidget(widget)

    def plots_math(self):
        widget = PlotsMath(self.settings, self.database)
        self.ui.stackedWidget.addWidget(widget)
        self.ui.stackedWidget.setCurrentWidget(widget)


    def open_fits(self, filename, type):
        file = os.path.realpath(filename)
        self.settings.setValue(type + "_last_dir", os.path.dirname(file))
        self.settings.setValue(type + "_last_file", file)
        return fits.open(file)

    def finish_spectrum(self, file):
        fits_file = self.open_fits(file[0], 'open_spectrum')
        widget = FinishSpectrum(fits_file, self.settings, self.database)
        self.ui.stackedWidget.addWidget(widget)
        self.ui.stackedWidget.setCurrentWidget(widget)