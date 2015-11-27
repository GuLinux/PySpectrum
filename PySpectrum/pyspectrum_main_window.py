from ui_pyspectrum_main_window import Ui_PySpectrumMainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from import_image import ImportImage
from PyQt5.QtCore import QSettings
import os

class PySpectrumMainWindow(QMainWindow):
    def __init__(self):
        super(PySpectrumMainWindow, self).__init__()
        self.ui = Ui_PySpectrumMainWindow()
        self.ui.setupUi(self)
        self.settings = QSettings("GuLinux", "PySpectrum")
        self.ui.actionOpen_Image.triggered.connect(self.open_image)
        
    def open_image(self):
        file = QFileDialog.getOpenFileName(self, "Open FITS Image", self.settings.value("last_open_image_dir", type=str), "FITS Images (*.fit *.fits)")[0]
        if not file:
            return
        file = os.path.realpath(file)
        self.settings.setValue("last_open_image_dir", os.path.dirname(file))
