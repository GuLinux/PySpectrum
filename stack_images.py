from pyui.stack_images import Ui_StackImages
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
from matplotlib.patches import Rectangle
from rotate_image_dialog import RotateImageDialog

class StackImages(QWidget):
    def __init__(self, fits_file, settings):
        QWidget.__init__(self)
        self.fits_file = fits_file
        self.ui = Ui_StackImages()
        self.ui.setupUi(self)
        self.settings = settings
        self.degrees = 0. # TODO 
        self.files_model = QStandardItemModel()
        self.files_model.setHorizontalHeaderLabels(['File', 'Quality', 'Align'])
        self.ui.files.setModel(self.files_model)
        self.__add_file_to_model(fits_file)
        self.plot = QtCommons.nestWidget(self.ui.plot, QImPlotWidget(self.__files_data()[0]['data'], cmap='gray'))
        self.__set_ref(0)
        self.toolbar = QToolBar()
        self.add = self.toolbar.addAction('Add', lambda: open_files_sticky('Open FITS Images',FITS_IMG_EXTS, self.__open, settings, IMPORT_IMG, parent=self ))
        self.remove = self.toolbar.addAction('Remove', self.__remove_selected_rows)
        self.reference_action = self.toolbar.addAction('Reference', lambda: self.__set_ref(self.ui.files.selectionModel().selectedRows()[0].row() ) )
        self.toolbar.addAction('Select alignment region', lambda: self.plot.add_rectangle_selector('select_align', self.__alignment_region_selected))
        self.toolbar.addAction('Rotate', lambda: self.rotate_dialog.show() )
        self.ui.files.selectionModel().selectionChanged.connect(lambda sel, unsel: self.__selection_changed() )
        self.ui.files.clicked.connect(lambda index: self.__draw_image(index.row()))
        #self.accepted.connect(self.stack)
        self.__selection_changed()
        
    def __selection_changed(self):
        sel = len(self.ui.files.selectionModel().selectedRows())
        self.remove.setEnabled(sel)
        self.reference_action.setEnabled(sel == 1)
        
    def __draw_image(self,index):
        image_view = self.plot.axes_image
        image_view.set_data(self.files_model.item(index).data()['data'])
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
    
    def __add_file_to_model(self, fits_file):
        item = QStandardItem(os.path.basename(fits_file.filename()))
        data = fits_file[0].data
        data = scipy.ndimage.interpolation.rotate(data, self.degrees, reshape=True, order=5, mode='constant')
        spatial = data.sum(1)
        profile = data.sum(0)
        roots = UnivariateSpline(range(0, len(spatial)), spatial-np.max(spatial)/2, s=0.2, k=3).roots()
        quality = roots[1]-roots[0]
        item.setData({'file': fits_file.filename(), 'fits': fits_file, 'data': data, 'spatial': spatial, 'profile': profile, 'quality': quality})
        
        offset = QStandardItem('N/A') # TODO

        quality_item = QStandardItem("")
        self.files_model.appendRow([item, quality_item, offset])
        return item
    
    def __add_file(self, fits_file):
        item = self.__add_file_to_model(fits_file)
        if self.files_model.rowCount() == 1:
            self.__set_ref(0)
        else:
            self.align(item.data())
        self.__update_qualities()
        
    def __update_qualities(self):
        qualities = [d['quality'] for d in self.__files_data()]
        self.qualities = (min(qualities), max(qualities))
        for index in range(0, self.files_model.rowCount()):
            self.files_model.item(index, 1).setText("{}%".format(self.__quality_percent(self.files_model.item(index).data()['quality'])))
        
    def __quality_percent(self, quality):
        return 100. - (100. * (quality-self.qualities[0]) / (self.qualities[1]-self.qualities[0]))
        
    def align(self, data):
        if data['file'] == self.reference['file']:
            self.__update_offset(data, (0, 0))
            return
        print("{} shape: {}".format(data['file'], data['data'].shape))
        offset_range = lambda n: range(1-int(n), int(n)-1)
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
        for row in sorted([r.row() for r in self.ui.files.selectionModel().selectedRows()], reverse=True):
            self.files_model.removeRows(row, 1)
        if self.files_model.rowCount() == 0:
            return
        if len([f for f in self.__files_data() if f['file'] == self.reference['file']]) == 0:
            self.__set_ref(0)
            
    def __set_ref(self, index):
        self.reference = self.files_model.item(index).data()
        self.rotate_dialog = RotateImageDialog(self.fits_file, 0)
        self.rotate_dialog.rotated.connect(self.__rotated)
        print("*ref: {} shape: {}".format(self.reference['file'], self.reference['data'].shape))
        indexes = lambda data: (int(len(data)/4), int(len(data)/4*3))
        self.__set_reference_indexes(indexes(self.reference['profile']), indexes(self.reference['spatial']) )
        #self.reference_indexes = { 'h': indexes(self.reference['profile']), 'v': indexes(self.reference['spatial']) }
        for data in self.__files_data() :
            self.align(data)
            
    def __rotated(self):
        self.degrees = self.rotate_dialog.degrees()
        for index in range(0, self.files_model.rowCount()):
            self.files_model.removeRow(index)
        self.__add_file(self.fits_file)
        self.__draw_image(0)
            
    def __alignment_region_selected(self, eclick, erelease):
        self.__set_reference_indexes((eclick.xdata, erelease.xdata), (eclick.ydata, erelease.ydata))
        
    def __set_reference_indexes(self, x, y):
        self.reference_indexes = { 'h': x, 'v': y }
        self.__draw_reference_rect()
        
    def __draw_reference_rect(self):
        self.plot.rm_element('reference_indexes')
        x, y = self.reference_indexes['h'], self.reference_indexes['v']
        rect = Rectangle((x[0], y[0]), x[1]-x[0], y[1]-y[0], fill=True, alpha=0.3, color='green')
        self.plot.figure.axes[0].add_artist(rect)
        self.plot.add_element(rect, 'reference_indexes')
        self.plot.figure.canvas.draw()
        
    def stack(self):
        dataset = self.__files_data()
        median = MedianStacker(dataset).median()
        self.fits_file[0].data = median
        
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
            