from ui_pyspectrum_main_window import Ui_PySpectrumMainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from import_image import ImportImage
from calibrate_spectrum import CalibrateSpectrum
from PyQt5.QtCore import QSettings
import os
from astropy.io import fits
from qtcommons import QtCommons

class PySpectrumMainWindow(QMainWindow):
    def __init__(self):
        super(PySpectrumMainWindow, self).__init__()
        self.ui = Ui_PySpectrumMainWindow()
        self.ui.setupUi(self)
        self.settings = QSettings("GuLinux", "PySpectrum")
        self.ui.actionOpen_Image.triggered.connect(lambda: QtCommons.open_file('Open FITS Image',"FITS Images (*.fit *.fits)", self.open_image, self.settings.value("open_image_last_dir", type=str) ))
        self.ui.actionCalibrate_FITS.triggered.connect(lambda: QtCommons.open_file('Open raw FITS Spectrum',"FITS Images (*.fit *.fits)", self.calibrate, self.settings.value("spectrum_last_dir", type=str) ))
        self.ui.stackedWidget.currentChanged.connect(self.current_changed)
        self.current_widget_toolbar = None
        
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
        widget = CalibrateSpectrum(fits_file, self.settings)
        self.ui.stackedWidget.addWidget(widget)
        self.ui.stackedWidget.setCurrentWidget(widget)



    def open_fits(self, filename, type):
        file = os.path.realpath(filename)
        self.settings.setValue(type + "_last_dir", os.path.dirname(file))
        self.settings.setValue(type + "_last_file", file)
        return fits.open(file)
