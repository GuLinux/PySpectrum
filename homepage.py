from pyui.homepage import Ui_HomePage
from PyQt5.QtWidgets import QApplication
from pyspectrum_commons import *
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from qtcommons import QtCommons
from PyQt5.QtWidgets import QWidget, QToolBar
from PyQt5.QtCore import Qt, QObject, pyqtSignal

class HomePage(QWidget):
    import_image = pyqtSignal(str)
    calibrate = pyqtSignal(str)
    math = pyqtSignal(str)
    finish = pyqtSignal(str)

    def __init__(self, settings):
        QWidget.__init__(self)
        self.ui = Ui_HomePage()
        self.ui.setupUi(self)
        self.toolbar = QToolBar()
        welcome_text = "{} {}".format(QApplication.instance().applicationName(), QApplication.instance().applicationVersion())
        self.ui.welcome_label.setText(self.ui.welcome_label.text().format(welcome_text))
        file_action = QtCommons.addToolbarPopup(self.toolbar, 'File')
        file_action.menu().addAction(QIcon(':/image_20'), 'Import Image', lambda: QtCommons.open_file_sticky('Open FITS Image',FITS_IMG_EXTS, lambda f: self.import_image.emit(f[0]), settings, IMPORT_IMG_DIR ))
        file_action.menu().addAction(QIcon(':/plot_20'), 'Calibrate Spectrum', lambda: QtCommons.open_file_sticky('Open raw FITS Spectrum',FITS_EXTS, lambda f: self.calibrate.emit(f[0]), settings, RAW_PROFILE_DIR, [IMPORT_IMG_DIR] ))
        file_action.menu().addAction(QIcon(':/math_20'), 'Spectra Math', lambda: self.math.emit(None) )
        file_action.menu().addAction(QIcon(':/done_20'), 'Finish Spectrum', lambda: QtCommons.open_file_sticky('Open FITS Spectrum',FITS_EXTS, lambda f: self.finish.emit(f[0]), settings, CALIBRATED_PROFILE_DIR, [RAW_PROFILE_DIR,IMPORT_IMG_DIR] ))

