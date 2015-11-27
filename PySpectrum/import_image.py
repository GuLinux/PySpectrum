from ui_import_image import Ui_ImportImage
from PyQt5.QtWidgets import QWidget

class ImportImage(QWidget):
    def __init__(self, fits_file):
        super(ImportImage, self).__init__()
        self.fits_file = fits_file
        self.ui = Ui_ImportImage()
        self.ui.setupUi(self)
