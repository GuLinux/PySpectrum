from ui_pyspectrum_main_window import Ui_PySpectrumMainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from import_image import ImportImage
from PyQt5.QtCore import QSettings
import os
from astropy.io import fits

class PySpectrumMainWindow(QMainWindow):
    def __init__(self):
        super(PySpectrumMainWindow, self).__init__()
        self.ui = Ui_PySpectrumMainWindow()
        self.ui.setupUi(self)
        self.settings = QSettings("GuLinux", "PySpectrum")
        self.ui.actionOpen_Image.triggered.connect(self.open_image)
        self.ui.stackedWidget.currentChanged.connect(self.current_changed)
        self.current_widget_toolbar = None
        
    def current_changed(self, index):
        if self.current_widget_toolbar:
            self.removeToolBar(self.current_widget_toolbar)
        self.current_widget_toolbar = self.ui.stackedWidget.currentWidget().toolbar
        self.addToolBar(self.current_widget_toolbar)
        
    def open_image(self):
        file = QFileDialog.getOpenFileName(self, "Open FITS Image", self.settings.value("open_image_last_dir", type=str), "FITS Images (*.fit *.fits)")[0]
        if not file:
            return
        fits_file = self.open_fits(file, "open_image")
        self.import_image = ImportImage(fits_file, self.settings)
        self.ui.stackedWidget.addWidget(self.import_image)
        self.ui.stackedWidget.setCurrentWidget(self.import_image)


    def open_fits(self, filename, type):
        file = os.path.realpath(filename)
        self.settings.setValue(type + "_last_dir", os.path.dirname(file))
        self.settings.setValue(type + "_last_file", file)
        return fits.open(file)
