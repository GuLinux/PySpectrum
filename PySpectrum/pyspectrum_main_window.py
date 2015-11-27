from ui_pyspectrum_main_window import Ui_PySpectrumMainWindow
from PyQt5.QtWidgets import QMainWindow
from import_image import ImportImage

class PySpectrumMainWindow(QMainWindow):
    def __init__(self):
        super(PySpectrumMainWindow, self).__init__()
        self.ui = Ui_PySpectrumMainWindow()
        self.ui.setupUi(self)
