from pyui.stack_images_dialog import Ui_StackImagesDialog
from PyQt5.QtWidgets import QDialog, QAction, QLineEdit, QFileDialog, QProgressDialog, QApplication, QToolBar
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
import numpy as np

class StackImagesDialog(QDialog):
    def __init__(self, fits_file, degrees, settings):
        QDialog.__init__(self)
        self.fits_file = fits_file
        self.ui = Ui_StackImagesDialog()
        self.ui.setupUi(self)
        self.settings = settings
        self.restoreGeometry(self.settings.value('stack_images_dialog', QByteArray()))
        self.degrees = degrees
        self.files_model = QStandardItemModel()
        self.ui.files.setModel(self.files_model)
        self.__add_file(fits_file)
        self.plot = QtCommons.nestWidget(self.ui.plot, QImPlotWidget(self.reference['data'], cmap='gray'))
        self.toolbar = QtCommons.nestWidget(self.ui.toolbar_wrapper, QToolBar())
        self.add = self.toolbar.addAction('Add', lambda: open_files_sticky('Open FITS Images',FITS_IMG_EXTS, self.__open, settings, IMPORT_IMG, parent=self ))
        self.remove = self.toolbar.addAction('Remove', self.__remove_selected_rows)
        self.reference_action = self.toolbar.addAction('Reference', lambda: self.__set_ref(self.ui.files.selectionModel().selectedRows()[0].row() ) )
        self.ui.files.selectionModel().selectionChanged.connect(lambda sel, unsel: self.__selection_changed() )
        self.ui.files.clicked.connect(self.__draw_image)
        self.accepted.connect(self.stack)
        self.__selection_changed()
        
    def __selection_changed(self):
        sel = len(self.ui.files.selectionModel().selectedRows())
        self.remove.setEnabled(sel)
        self.reference_action.setEnabled(sel == 1)
        
    def __draw_image(self,index):
        image_view = self.plot.axes_image
        image_view.set_data(self.files_model.item(index.row()).data()['data'])
        image_view.figure.canvas.draw()
        
    def __open(self, files):
        existing_files = [d['file'] for d in self.__files_data()]
        progress = QProgressDialog("Loading files", None, 0, len(files), self);
        progress.setWindowModality(Qt.WindowModal);
        progress.show()
        for index, file in enumerate(files):
            progress.setValue(index+1)
            QApplication.instance().processEvents()
            if file not in existing_files:
                self.__add_file(fits.open(file))
        
    def __row_index(self, data):
        return [i for i, d in enumerate(self.__files_data()) if d['file'] == data['file']][0]
    
    def __add_file(self, fits_file):
        item = QStandardItem(os.path.basename(fits_file.filename()))
        data = fits_file[0].data
        data = scipy.ndimage.interpolation.rotate(data, self.degrees, reshape=True, order=5, mode='constant')
        spatial = data.sum(1)
        profile = data.sum(0)
        item.setData({'file': fits_file.filename(), 'fits': fits_file, 'data': data, 'spatial': spatial, 'profile': profile})
        roots = UnivariateSpline(range(0, len(spatial)), spatial-np.max(spatial)/2, s=0.2, k=3).roots()
        offset = QStandardItem('N/A') # TODO

        quality = QStandardItem("{}".format(4/(roots[-1]-roots[0])) )
        self.files_model.appendRow([item, quality, offset])
        if self.files_model.rowCount() == 1:
            self.__set_ref(0)
        else:
            self.align(item.data())
        
    def align(self, data):
        if data['file'] == self.reference['file']:
            self.__update_offset(data, (0, 0))
            return
        offset_range = lambda n: range(1-n, n-1)
        offsets = lambda name, indexes: [ (pearsonr(self.reference[name][indexes[0]:indexes[1]], data[name][indexes[0]-offset:indexes[1]-offset] )[0], offset) for offset in offset_range(indexes[0]) ]
        x_offset = sorted(offsets('profile', self.reference_indexes['h']), key=lambda x: x[0])[-1]
        y_offset = sorted(offsets('spatial', self.reference_indexes['v']), key=lambda y: y[0])[-1]
        self.__update_offset(data, (x_offset[1], y_offset[1]))
        
    def __update_offset(self, data, offset):
        row = self.__row_index(data)
        self.files_model.item(row, 2).setText('{}, {}'.format(offset[0], offset[1]))
        data.update({'offset': {'x': offset[0], 'y': offset[1]}})
        self.files_model.item(row).setData(data)
        
    def __files_data(self):
        return [self.files_model.item(i).data() for i in range(0, self.files_model.rowCount())]
        
    def __remove_selected_rows(self):
        for row in [r.row() for r in self.ui.files.selectionModel().selectedRows()]:
            self.files_model.removeRows(row, 1)
        if self.files_model.rowCount() == 0:
            return
        if len([f for f in self.__files_data() if f['file'] == self.reference['file']]) == 0:
            self.__set_ref(0)
            
    def __set_ref(self, index):
        self.reference = self.files_model.item(index).data()
        indexes = lambda data: (int(len(data)/4), int(len(data)/4*3))
        self.reference_indexes = { 'h': indexes(self.reference['profile']), 'v': indexes(self.reference['spatial']) }
        for data in self.__files_data() :
            self.align(data)
        
    def closeEvent(self, ev):
        self.settings.setValue('stack_images_dialog', self.saveGeometry())
        QDialog.closeEvent(self, ev)
        
    def stack(self):
        dataset = self.__files_data()
        offsets = ([x['offset']['x'] for x in dataset], [y['offset']['y'] for y in dataset])
        shape = dataset[0]['data'].shape
        offsets = (min(offsets[0]), max(offsets[0]), min(offsets[1]), max(offsets[1]))
        print(offsets)
        #base_indexes = (0-offsets[0[, shape[0])
        #for data in datasets:
        #    print('{}, {}'.format(data['offset']['x'], data['offset']['y']))
        self.fits_file[0].data = np.median([i['data'] for i in self.__files_data()], axis=0)
        
class MedianStacker:
    def __init__(self, matrices):
        self.matrices = matrices
        
    def final_shape(self):
        offsets = ( [y['offset']['y'] for y in self.matrices], [x['offset']['x'] for x in self.matrices] )
        offsets = (min(offsets[0]), max(offsets[0]), min(offsets[1]), max(offsets[1]))
        shape = self.matrices[0]['data'].shape
        return {'shape': (shape[0] - offsets[0] + offsets[1], shape[1] - offsets[2] + offsets[3]), 'zero': (-offsets[0],-offsets[2]) }
    
    def data_reposition(self, data, shape_offset):
        shape = shape_offset['shape']
        ret = np.zeros(shape[0]*shape[1]).reshape(shape)
        rows_offset = data['offset']['y'] + shape_offset['zero'][0]
        cols_offset = data['offset']['x'] + shape_offset['zero'][1]

        rows = [rows_offset, data['data'].shape[0] + rows_offset]
        cols = [cols_offset, data['data'].shape[1] + cols_offset]
        ret[rows[0]:rows[1], cols[0]:cols[1]] = data['data']
        return ret
        
    def median(self):
        final_shape = self.final_shape()
        data = np.array([self.data_reposition(d, final_shape) for d in self.matrices])
        return np.median(data, axis=0)
            