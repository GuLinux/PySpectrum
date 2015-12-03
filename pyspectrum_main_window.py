from pyui.pyspectrum_main_window import Ui_PySpectrumMainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
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
import resources.resources

class PySpectrumMainWindow(QMainWindow):
    def __init__(self):
        font = QApplication.instance().font()
        rc('font', **{'family':'serif','serif':[font.defaultFamily()]})
        super(PySpectrumMainWindow, self).__init__()
        self.ui = Ui_PySpectrumMainWindow()
        self.database = sqlite3.connect('data/pyspectrum.db')
        self.ui.setupUi(self)
        self.settings = QSettings("GuLinux", "PySpectrum")
        QtCommons.addToolbarPopup(self.ui.toolBar, 'File', actions=[self.ui.actionOpen_Image,self.ui.actionCalibrate_FITS,self.ui.actionPlots_Math,self.ui.actionFinish_Spectrum])
        self.actionClose = self.ui.toolBar.addAction(QIcon(':/close_20'), "Close")
        self.ui.actionOpen_Image.setIcon(QIcon(':/image_20'))
        self.ui.actionCalibrate_FITS.setIcon(QIcon(':/plot_20'))
        self.ui.actionPlots_Math.setIcon(QIcon(':/math_20'))
        self.ui.actionFinish_Spectrum.setIcon(QIcon(':/done_20'))
        self.actionClose.setEnabled(False)
        self.actionClose.triggered.connect(self.close_widget)
        self.ui.actionOpen_Image.triggered.connect(lambda: QtCommons.open_file_sticky('Open FITS Image',FITS_IMG_EXTS, self.open_image, self.settings, IMPORT_IMG_DIR ))
        self.ui.actionCalibrate_FITS.triggered.connect(lambda: QtCommons.open_file_sticky('Open raw FITS Spectrum',FITS_EXTS, self.calibrate, self.settings, RAW_PROFILE_DIR, [IMPORT_IMG_DIR] ))
        self.ui.actionPlots_Math.triggered.connect(self.plots_math)
        self.ui.actionFinish_Spectrum.triggered.connect(lambda: QtCommons.open_file_sticky('Open FITS Spectrum',FITS_EXTS, self.finish_spectrum, self.settings, CALIBRATED_PROFILE_DIR, [RAW_PROFILE_DIR,IMPORT_IMG_DIR] ))
        self.ui.stackedWidget.currentChanged.connect(self.current_changed)
        self.current_widget_toolbar = None
        self.restoreGeometry(self.settings.value('window_geometry', QByteArray()))
        
    def closeEvent(self, ev):
        self.settings.setValue('window_geometry', self.saveGeometry())
        QMainWindow.closeEvent(self, ev)
        
    def close_widget(self):
        # TODO: close() on widget
        self.ui.stackedWidget.currentWidget().deleteLater()
        
    def current_changed(self, index):
        print(index)
        self.actionClose.setEnabled(index > 1)
        if self.current_widget_toolbar:
            self.removeToolBar(self.current_widget_toolbar)
        if index > 1:
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
        return fits.open(file)

    def finish_spectrum(self, file):
        fits_file = self.open_fits(file[0], 'open_spectrum')
        widget = FinishSpectrum(fits_file, self.settings, self.database)
        self.ui.stackedWidget.addWidget(widget)
        self.ui.stackedWidget.setCurrentWidget(widget)