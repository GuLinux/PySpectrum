from pyui.stack_images_dialog import Ui_StackImagesDialog
from PyQt5.QtWidgets import QDialog, QAction, QLineEdit, QFileDialog, QProgressDialog, QApplication
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QStandardPaths, QByteArray
from pyspectrum_commons import *
from project import Project
from astropy.io import fits
import scipy.ndimage.interpolation
from qmathplotwidget import QMathPlotWidget, QImPlotWidget
import os
from scipy.stats import pearsonr
from scipy.interpolate import UnivariateSpline

class StackImagesDialog(QDialog):
    def __init__(self, fits_file, degrees, settings):
        QDialog.__init__(self)
        self.ui = Ui_StackImagesDialog()
        self.ui.setupUi(self)
        self.settings = settings
        self.restoreGeometry(self.settings.value('stack_images_dialog', QByteArray()))
        self.degrees = degrees
        self.files_model = QStandardItemModel()
        self.ui.files.setModel(self.files_model)
        self.__add_file(fits_file)
        self.plot = QtCommons.nestWidget(self.ui.plot, QImPlotWidget(self.reference['data'], cmap='gray'))
        self.ui.files.selectionModel().selectionChanged.connect(self.__selection_changed)
        self.ui.files.clicked.connect(self.__draw_image)
        self.ui.add.clicked.connect(lambda: open_files_sticky('Open FITS Images',FITS_IMG_EXTS, self.__open, settings, IMPORT_IMG, parent=self ))
        
    def __selection_changed(self, sel, unsel):
        self.ui.remove.setEnabled(len(sel.indexes()))
        self.ui.reference.setEnabled(len(sel.indexes()) == 1)
        
    def __draw_image(self,index):
        image_view = self.plot.axes_image
        image_view.set_data(self.files_model.item(index.row()).data()['data'])
        image_view.figure.canvas.draw()
        
    def __open(self, files):
        existing_files = [self.files_model.item(i).data()['file'] for i in range(0, self.files_model.rowCount())]
        progress = QProgressDialog("Loading files", None, 0, len(files), self);
        progress.setWindowModality(Qt.WindowModal);
        progress.show()
        for index, file in enumerate(files):
            progress.setValue(index+1)
            QApplication.instance().processEvents()
            if file not in existing_files:
                self.__add_file(fits.open(file))
        
    def __add_file(self, fits_file):
        item = QStandardItem(os.path.basename(fits_file.filename()))
        data = fits_file[0].data
        data = scipy.ndimage.interpolation.rotate(data, self.degrees, reshape=True, order=5, mode='constant')
        spatial = data.sum(1)
        profile = data.sum(0)
        item.setData({'file': fits_file.filename(), 'fits': fits_file, 'data': data, 'spatial': spatial, 'profile': profile})
        roots = UnivariateSpline(range(0, len(profile)), profile, s=0.5, k=3).roots()
        offset = QStandardItem('N/A') # TODO
        print(roots)
        quality = QStandardItem("{}".format(roots[1]-roots[0]) )
        self.files_model.appendRow([item, quality, offset])
        if self.files_model.rowCount() == 1:
            self.__set_ref(0)
        else:
            # Calculate offset
            pass
        
    def __set_ref(self, index):
        self.reference = self.files_model.item(index).data()
        self.start_index = len(self.reference)/4
        self.end = len(self.reference)/4*3
        
    def closeEvent(self, ev):
        self.settings.setValue('stack_images_dialog', self.saveGeometry())
        QDialog.closeEvent(self, ev)