from pyui.stack_images_dialog import Ui_StackImagesDialog
from PyQt5.QtWidgets import QDialog, QAction, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QStandardPaths
from pyspectrum_commons import *
from project import Project

class StackImagesDialog(QDialog):
    def __init__(self, fits_file):
        QDialog.__init__(self)
        self.ui = Ui_StackImagesDialog()
        self.ui.setupUi(self)