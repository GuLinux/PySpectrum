from ui_plots_math import Ui_PlotsMath
from scipy.interpolate import *
from qmathplotwidget import QMathPlotWidget
from PyQt5.QtWidgets import QWidget, QToolBar, QToolButton, QMenu, QAction
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QByteArray, QTimer
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from fits_spectrum import FitsSpectrum
from qtcommons import QtCommons
import numpy as np
from astropy.io import fits
from miles import Miles
from miles_dialog import MilesDialog
from collections import deque
class PlotsMath(QWidget):
    
    F_X = Qt.UserRole + 1
    FITS_SPECTRUM = Qt.UserRole + 2
    
    def __init__(self, settings):
        super(PlotsMath, self).__init__()
        self.ui = Ui_PlotsMath()
        self.ui.setupUi(self)
        self.settings = settings
        self.plot = QtCommons.nestWidget(self.ui.plot, QMathPlotWidget())
        self.miles_dialog = MilesDialog()
        self.miles_dialog.fits_picked.connect(self.open_fits)
        self.toolbar = QToolBar('Instrument Response Toolbar')
        open_btn = QtCommons.addToolbarPopup(self.toolbar, text="Open...", icon_name='document-open')
        open_btn.menu().addAction('FITS file', lambda: QtCommons.open_file('Open FITS Spectrum',"FITS Images (*.fit *.fits)", lambda f: self.open_fits(f[0]), self.settings.value("open_spectrum_last_dir", type=str) ))
        open_btn.menu().addAction('MILES reference', self.miles_dialog.show)
        self.toolbar.addAction('Set operand', self.set_operand)
        self.toolbar.addSeparator()
        self.toolbar.addAction('Zoom', self.start_zoom)
        self.toolbar.addAction('Reset Zoom', lambda: self.plot.reset_zoom(self.x_axis, self.data.min(), self.data.max()) )
        self.toolbar.addSeparator()
        remove_btn = QtCommons.addToolbarPopup(self.toolbar, text='Remove...')
        remove_btn.menu().addAction(self.ui.actionSelectPointsToRemove)
        self.ui.actionSelectPointsToRemove.triggered.connect(self.pick_rm_points)
        self.undo_action = self.toolbar.addAction('Undo', self.undo )
        self.undo_action.setEnabled(False)
        self.ui.spline_factor.valueChanged.connect(self.factor_valueChanged)
        self.ui.spline_degrees.valueChanged.connect(lambda v: self.draw())
        self.ui.spline_factor_auto.toggled.connect(lambda v: self.draw())
        self.ui.spline_factor_auto.toggled.connect(lambda v: self.ui.spline_factor.setEnabled(not v))
        self.ui.execute.clicked.connect(self.execute_operation)
        self.operands_model = QStandardItemModel()
        self.ui.operands_listview.setModel(self.operands_model)
        self.undo_buffer = deque(maxlen=20)
        
    def undo(self):
        undo = self.undo_buffer.pop()
        self.x_axis = undo[0]
        self.data = undo[1]
        self.draw()
        self.undo_action.setEnabled(len(self.undo_buffer)>0)
        
    def store_undo(self):
        self.undo_buffer.append((np.copy(self.x_axis), np.copy(self.data)))
        self.undo_action.setEnabled(True)

    def open_fits(self, filename):
        fits_file = fits.open(filename)
        self.fits_spectrum = FitsSpectrum(fits_file)
        self.x_axis = self.fits_spectrum.x_axis()
        self.data = self.fits_spectrum.data()
        self.data /= self.data.max()
        self.rect = [self.x_axis[0], self.x_axis[-1], 0, 1]
        self.draw()

    @pyqtSlot(float)
    def factor_valueChanged(self, f):
        self.draw()
        
    def pick_rm_points(self):
        self.plot.rm_element('zoom')
        self.plot.add_span_selector('pick_rm_points', lambda min,max: self.rm_points(min,max+1),direction='horizontal')
        
        
    def start_zoom(self):
        self.plot.rm_element('pick_rm_points')
        self.plot.select_zoom()
        
    def draw(self):
        self.ui.spline_degrees_value.setText("{}".format(self.ui.spline_degrees.value()))
        spline_factor = self.ui.spline_factor.value() if not self.ui.spline_factor_auto.isChecked() else None
        spline = UnivariateSpline(self.x_axis, self.data, k=self.ui.spline_degrees.value(), s=spline_factor)
        self.f_x = lambda x: spline(x)
        self.plot.plot(self.x_axis, self.data, '--', self.x_axis, spline(self.x_axis), '-')
        self.plot.figure.canvas.draw()
        
    def rm_points(self, min, max):
        self.store_undo()
        min = self.fits_spectrum.x_uncalibrated(min)
        max = self.fits_spectrum.x_uncalibrated(max)
        rect = lambda x: x*((self.data[max]-self.data[min])/(max-min)) + self.data[min]
        self.data[min:max] = np.fromfunction(rect, self.data[min:max].shape)
        self.draw()
        self.plot.rm_element('pick_rm_points')
        
    def set_operand(self):
        item = QStandardItem(self.fits_spectrum.name())
        item.setData(self.f_x, PlotsMath.F_X)
        item.setData(self.fits_spectrum, PlotsMath.FITS_SPECTRUM)
        self.operands_model.appendRow(item)
        
    def execute_operation(self):
        a = self.operands_model.item(0).data(PlotsMath.FITS_SPECTRUM)
        b = self.operands_model.item(1).data(PlotsMath.FITS_SPECTRUM)
        self.x_axis=np.arange(max(a.x_axis()[0], b.x_axis()[0]), min(a.x_axis()[-1],b.x_axis()[-1],))
        f_x_a = self.operands_model.item(0).data(PlotsMath.F_X)
        f_x_b = self.operands_model.item(1).data(PlotsMath.F_X)
        data_f1 =  np.fromfunction(lambda x: f_x_a(x+self.x_axis[0]), self.x_axis.shape)
        data_f2 =  np.fromfunction(lambda x: f_x_b(x+self.x_axis[0]), self.x_axis.shape)
        self.data = data_f1/data_f2
        self.plot.plot(self.x_axis, data_f1, '-', self.x_axis, data_f2, "-", self.x_axis, self.data)
        self.plot.figure.canvas.draw()
        
    def save(self):
        pass
        