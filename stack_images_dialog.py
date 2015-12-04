from pyui.stack_images_dialog import Ui_StackImagesDialog
from PyQt5.QtWidgets import QDialog, QAction, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QStandardPaths
from pyspectrum_commons import *
from project import Project
import scipy.ndimage.interpolation
from qmathplotwidget import QMathPlotWidget, QImPlotWidget
import os

class StackImagesDialog(QDialog):
    def __init__(self, fits_file, degrees):
        QDialog.__init__(self)
        self.ui = Ui_StackImagesDialog()
        self.ui.setupUi(self)
        self.degrees = degrees
        self.files_model = QStandardItemModel()
        self.ui.files.setModel(self.files_model)
        self.__add_file(fits_file)
        self.plot = QtCommons.nestWidget(self.ui.plot, QImPlotWidget(self.reference['data'], cmap='gray'))
        
    def __add_file(self, fits_file):
        item = QStandardItem(os.path.basename(fits_file.filename()))
        data = fits_file[0].data
        data = scipy.ndimage.interpolation.rotate(data, self.degrees, reshape=True, order=5, mode='constant')
        spatial = data.sum(1)
        profile = data.sum(0)
        item.setData({'fits': fits_file, 'data': data, 'spatial': spatial, 'profile': profile})
        self.files_model.appendRow(item)
        if self.files_model.rowCount() == 1:
            self.__set_ref(0)
        
    def __set_ref(self, index):
        self.reference = self.files_model.item(index).data()