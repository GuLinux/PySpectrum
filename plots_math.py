from pyui.plots_math import Ui_PlotsMath
from scipy.interpolate import *
from qmathplotwidget import QMathPlotWidget
from PyQt5.QtWidgets import QWidget, QToolBar, QToolButton, QMenu, QAction, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QByteArray, QTimer
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from fits_spectrum import FitsSpectrum, Spectrum
from qtcommons import QtCommons
import numpy as np
from astropy.io import fits
from collections import deque
from pyspectrum_commons import *
from reference_spectra_dialog import ReferenceSpectraDialog

class PlotsMath(QWidget):
    
    F_X = Qt.UserRole + 1
    FITS_SPECTRUM = Qt.UserRole + 2
    
    def __init__(self, settings, database):
        super(PlotsMath, self).__init__()
        self.ui = Ui_PlotsMath()
        self.ui.setupUi(self)
        self.settings = settings
        self.plot = QtCommons.nestWidget(self.ui.plot, QMathPlotWidget())
        self.reference_dialog = ReferenceSpectraDialog(database)
        self.reference_dialog.fits_picked.connect(self.open_fits)
        self.toolbar = QToolBar('Instrument Response Toolbar')
        open_btn = QtCommons.addToolbarPopup(self.toolbar, text="Open...", icon_file=':/new_open_20')
        open_btn.menu().addAction('FITS file', lambda: open_file_sticky('Open FITS Spectrum',FITS_EXTS, lambda f: self.open_fits(f[0]), self.settings, CALIBRATED_PROFILE, [RAW_PROFILE]))
        open_btn.menu().addAction('Reference library', self.reference_dialog.show)
        self.save_result = self.toolbar.addAction(QIcon(':/save_20'), 'Save', lambda: save_file_sticky('Save Operation Result...', 'FITS file (.fit)', self.save, self.settings, MATH_OPERATION, [CALIBRATED_PROFILE]))
        self.toolbar.addAction('Set operand', self.set_operand)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.ui.actionZoom)
        self.ui.actionZoom.triggered.connect(self.start_zoom)
        self.toolbar.addAction(self.ui.actionReset_Zoom)
        self.ui.actionReset_Zoom.triggered.connect(self.reset_zoom)
        self.toolbar.addSeparator()
        self.operands_model = QStandardItemModel()
        self.ui.operands_listview.setModel(self.operands_model)
        remove_btn = QtCommons.addToolbarPopup(self.toolbar, text='Remove...')
        remove_btn.menu().addAction(self.ui.actionSelectPointsToRemove)
        remove_btn.menu().addAction("Before point", lambda: spectrum_trim_dialog(self.spectrum, 'before', self.plot.axes, lambda: self.draw()))
        remove_btn.menu().addAction("After point", lambda: spectrum_trim_dialog(self.spectrum, 'after', self.plot.axes, lambda: self.draw()))
        self.ui.clear_operands.clicked.connect(self.operands_model.clear)
        self.ui.remove_operand.clicked.connect(lambda: self.operands_model.removeRows(self.ui.operands_listview.selectionModel().selectedRows()[0].row(), 1))
            
        self.operands_model.rowsInserted.connect(lambda: self.ui.clear_operands.setEnabled(self.operands_model.rowCount() > 0) )
        self.operands_model.rowsRemoved.connect(lambda: self.ui.clear_operands.setEnabled(self.operands_model.rowCount() > 0) )
        self.ui.operands_listview.selectionModel().selectionChanged.connect(lambda s, u: self.ui.remove_operand.setEnabled(len(s)))
        self.ui.actionSelectPointsToRemove.triggered.connect(self.pick_rm_points)
        self.toolbar.addAction(self.ui.actionUndo)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionUndo.setEnabled(False)
        self.ui.spline_factor.valueChanged.connect(self.factor_valueChanged)
        self.ui.spline_degrees.valueChanged.connect(lambda v: self.draw())
        self.ui.spline_factor_auto.toggled.connect(lambda v: self.draw())
        self.ui.spline_factor_auto.toggled.connect(lambda v: self.ui.spline_factor.setEnabled(not v))
        self.ui.execute.clicked.connect(self.execute_operation)
        self.plot.figure.tight_layout()
        self.undo_buffer = deque(maxlen=20)
        
    def undo(self):
        undo = self.undo_buffer.pop()
        self.spectrum.wavelengths = undo[0]
        self.spectrum.fluxes = undo[1]
        self.draw()
        self.ui.actionUndo.setEnabled(len(self.undo_buffer)>0)
        
    def store_undo(self):
        self.undo_buffer.append((np.copy(self.spectrum.wavelengths), np.copy(self.spectrum.fluxes)))
        self.ui.actionUndo.setEnabled(True)

    def open_fits(self, filename):
        fits_file = fits.open(filename)
        self.fits_spectrum = FitsSpectrum(fits_file)
        self.spectrum = self.fits_spectrum.spectrum
        self.spectrum.normalize_to_max()
        if self.spectrum.dispersion() <0.5:
            print("dispersion too high ({}), reducing spectrum resolution".format(self.spectrum.dispersion()))
            spline = InterpolatedUnivariateSpline(self.spectrum.wavelengths, self.spectrum.fluxes)
            self.spectrum.wavelengths = np.arange(self.spectrum.wavelengths[0], self.spectrum.wavelengths[-1], 0.5)
            self.spectrum.fluxes = np.fromfunction(lambda x: spline(x+self.spectrum.wavelengths[0]), self.spectrum.wavelengths.shape)
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
        spline = UnivariateSpline(self.spectrum.wavelengths, self.spectrum.fluxes, k=self.ui.spline_degrees.value(), s=spline_factor)
        self.f_x = lambda x: spline(x)
        self.plot.plot(None, self.spectrum.wavelengths, self.spectrum.fluxes, '--', self.spectrum.wavelengths, spline(self.spectrum.wavelengths), '-')
        self.plot.figure.tight_layout()
        self.plot.figure.canvas.draw()
        
    def rm_points(self, wmin, wmax):
        self.store_undo()
        x_min = self.spectrum.wavelength_index(max(self.spectrum.wavelengths[0], wmin))
        x_max = self.spectrum.wavelength_index(min(self.spectrum.wavelengths[-1], wmax))
        m=(self.spectrum.fluxes[x_max]-self.spectrum.fluxes[x_min])/(x_max-x_min)
        q = self.spectrum.fluxes[x_min]
        
        f = lambda x: x * m + q
        self.spectrum.fluxes[x_min:x_max] = np.fromfunction(f, self.spectrum.fluxes[x_min:x_max].shape)
        self.draw()
        self.plot.rm_element('pick_rm_points')
        
    def trim(self, direction):
        point = QInputDialog.getInt(None, 'Trim curve', 'Enter wavelength for trimming', self.spectrum.wavelengths[0] if direction == 'before' else self.spectrum.wavelengths[-1], self.spectrum.wavelengths[0], self.spectrum.wavelengths[-1])
        if not point[1]:
            return
        self.store_undo()
        if direction == 'before':
            self.spectrum.cut(start=self.spectrum.wavelength_index(point[0]))
        else:
            self.spectrum.cut(end=self.spectrum.wavelength_index(point[0]))
        self.reset_zoom()
        self.draw()
    
    def set_operand(self):
        item = QStandardItem(self.fits_spectrum.name())
        item.setData(self.f_x, PlotsMath.F_X)
        item.setData(self.spectrum, PlotsMath.FITS_SPECTRUM)
        self.operands_model.appendRow(item)
        
    def execute_operation(self):
        max_wavelengths = lambda operands: np.arange(max([o[0].wavelengths[0] for o in operands]), min([o[0].wavelengths[-1] for o in operands]))
        datasets = lambda operands, wavelengths: [np.fromfunction(lambda x: o[1](x+wavelengths[0]), wavelengths.shape) for o in operands]
        operands = [(self.operands_model.item(a).data(PlotsMath.FITS_SPECTRUM), self.operands_model.item(a).data(PlotsMath.F_X)) for a in np.arange(self.operands_model.rowCount())]
        
        
        def divide(operands):
            if len(operands) > 2:
                print("Division supports only 2 operands, truncating")
            wavelengths = max_wavelengths(operands[0:2])
            datas = datasets(operands[0:2], wavelengths)
            return (wavelengths, datas[0]/datas[1])
        
        def mean(operands):
            wavelengths = max_wavelengths(operands)
            mean_data = np.zeros(wavelengths.shape)
            for data in datasets(operands, wavelengths):
                mean_data += data
            return (wavelengths, mean_data/len(wavelengths))
        
        operations = { 0: divide, 1: mean }
        try:
            wavelengths, data = operations[self.ui.operation_type.currentIndex()](operands)
            self.spectrum = Spectrum(data, wavelengths)
            
            self.spectrum.normalize_to_max()
            self.draw()
        except IndexError:
            QMessageBox.warning(None, "Error", "Datasets are not compatible. Maybe you need to calibrate better, or use a different reference file")

    def save(self, filename):
        hdu = fits.PrimaryHDU(self.spectrum.fluxes)
        fits_file = fits.HDUList([hdu])
        hdu.header['CRPIX1'] = 1
        hdu.header['CRVAL1'] = self.spectrum.wavelengths[0]
        hdu.header['CDELT1'] = self.spectrum.dispersion()
        hdu.writeto(filename[0], clobber=True)

    def reset_zoom(self):
        self.plot.reset_zoom(self.spectrum.wavelengths, self.spectrum.fluxes.min(), self.spectrum.fluxes.max())
