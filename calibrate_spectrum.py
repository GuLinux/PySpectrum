from ui_calibrate_spectrum import Ui_CalibrateSpectrum
from PyQt5.QtWidgets import QWidget, QToolBar, QDialog, QDialogButtonBox, QFileDialog, QMenu, QAction
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from qmathplotwidget import QMathPlotWidget, QImPlotWidget
import matplotlib.pyplot as plt
from qtcommons import QtCommons
import scipy.ndimage.interpolation
from ui_rotate_image_dialog import Ui_RotateImageDialog
import os
import numpy as np
from astropy.io import fits
from fits_spectrum import FitsSpectrum
from matplotlib.widgets import SpanSelector
from matplotlib.lines import Line2D
from miles import Miles
from miles_dialog import MilesDialog

class CalibrateSpectrum(QWidget):
    def __init__(self, fits_file, config):
        super(CalibrateSpectrum, self).__init__()
        self.config = config
        self.fits_spectrum = FitsSpectrum(fits_file)
        self.fits_file = fits_file
        self.ui = Ui_CalibrateSpectrum()
        self.ui.setupUi(self)
        self.toolbar = QToolBar('Calibration Toolbar')
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.ui.x_axis_pick.setMenu(QMenu())
        self.ui.x_axis_pick.menu().addAction("Maximum from range").triggered.connect(lambda: self.pick_from_range('maximum'))
        self.ui.x_axis_pick.menu().addAction("Minimum from range").triggered.connect(lambda: self.pick_from_range('minimum'))
        self.ui.x_axis_pick.menu().addAction("Central value from range").triggered.connect(lambda: self.pick_from_range('central'))
        #self.ui.x_axis_pick.menu().addAction("Point")
        self.miles_dialog = MilesDialog()
        self.miles_dialog.fits_picked.connect(self.open_reference)
        save_action = self.toolbar.addAction(QIcon.fromTheme('document-save'), 'Save')
        reference_action = self.toolbar.addAction('Reference')
        reference_action.setMenu(QMenu())
        reference_from_file = reference_action.menu().addAction("Load from FITS file")
        reference_miles = reference_action.menu().addAction("MILES library")
        reference_miles.triggered.connect(lambda: self.miles_dialog.show())
        reference_from_file.triggered.connect(lambda: QtCommons.open_file('Open Reference Profile', "FITS Images (*.fit *.fits)", lambda f: self.open_reference(f[0])))
        #reference_action.setEnabled(false)
        self.spectrum_plot = QtCommons.nestWidget(self.ui.spectrum_plot_widget, QMathPlotWidget())
        
        self.calibration_model = QStandardItemModel()
        self.calibration_model.setHorizontalHeaderLabels(["x-axis", "wavelength", "error"])
        self.calibration_model.rowsInserted.connect(self.calculate_calibration)
        self.calibration_model.rowsRemoved.connect(self.calculate_calibration)
        self.ui.calibration_points.setModel(self.calibration_model)
        self.ui.calibration_points.selectionModel().selectionChanged.connect(lambda selected, deselected: self.ui.remove_calibration_point.setEnabled(len(selected.indexes()) > 0)  )
        self.ui.add_calibration_point.clicked.connect(self.add_calibration_point)
        self.ui.remove_calibration_point.setEnabled(False)
        self.ui.remove_calibration_point.clicked.connect(self.remove_calibration_point)
        save_action.triggered.connect(self.save)
        self.ui.point_is_star.toggled.connect(lambda checked: self.ui.point_wavelength.setEnabled(not checked))
        self.fits_spectrum.plot_to(self.spectrum_plot.axes)
        self.translate_y = lambda y: y
        self.translate_x = lambda x: x
        hdu_calibration_points = [h for h in self.fits_file if h.name == 'CALIBRATION_DATA']
        if len(hdu_calibration_points) > 0:
            for point in hdu_calibration_points[-1].data:
                self.add_calibration_point_data(point[0], point[1])
                
    
    def open_reference(self, file):
        fits_spectrum = FitsSpectrum(fits.open(file))
        data = fits_spectrum.data()
        data /= data.max()
        line = Line2D(fits_spectrum.x_axis(), data, color='gray')
        self.spectrum_plot.axes.add_line(line)
        self.spectrum_plot.figure.canvas.draw()
        
    def picked_from_range(self, type, min, max):
        min=(self.translate_y(min))
        max=(self.translate_y(max))
        point = {
            'minimum': self.fits_spectrum.data()[min:max+1].argmin() + min,
            'maximum': self.fits_spectrum.data()[min:max+1].argmax() + min,
            'central': min+(max-min)/2
            }[type]
        self.ui.point_x_axis.setValue(point)
        self.spectrum_plot.rm_element('pick_x_axis')
        self.ui.point_wavelength.setValue(self.translate_x(point))
        self.spectrum_plot.add_line("x_axis_pick", self.translate_x(point), color='r')

    def pick_from_range(self, type):
        self.spectrum_plot.add_span_selector('pick_x_axis', lambda min,max: self.picked_from_range(type, min, max),direction='horizontal')

    def remove_calibration_point(self):
        self.calibration_model.removeRow(self.ui.calibration_points.selectionModel().selectedIndexes()[0].row())
    
    def add_calibration_point_data(self, x_value, wavelength):
        x_axis_item = QStandardItem("star" if x_value == 0 else "{}".format(x_value))
        x_axis_item.setData(x_value)
        wavelength_item = QStandardItem("{:.2f}".format(wavelength))
        wavelength_item.setData(wavelength)
        self.calibration_model.appendRow([x_axis_item, wavelength_item, QStandardItem("n/a")])
        self.spectrum_plot.rm_element('x_axis_pick')
        
    
    def add_calibration_point(self):
        self.add_calibration_point_data(self.ui.point_x_axis.value(), 0 if self.ui.point_is_star.isChecked() else self.ui.point_wavelength.value())

    def calibration_points(self):
        return [{'row': row, 'x': self.calibration_model.item(row, 0).data(), 'wavelength': self.calibration_model.item(row, 1).data()} for row in range(self.calibration_model.rowCount())]

    def calculate_calibration(self):
        if self.calibration_model.rowCount() < 2:
            self.translate_y = lambda y: y
            self.translate_x = lambda x: x
            self.fits_spectrum.calibrate(1, 0)
            self.fits_spectrum.plot_to(self.spectrum_plot.axes)
            return
        points = sorted(self.calibration_points(), key=lambda point: point['x'])
        m, q = np.polyfit([i['x'] for i in points], [i['wavelength'] for i in points], 1)
        self.translate_x = lambda x: m*x+q
        self.translate_y = lambda x: (x-q)/m
        self.ui.dispersion.setValue(m)
        for row, value in [(p['row'], "{:.2f}".format( p['wavelength']-self.translate_x(p['x']))) for p in points]:
            self.calibration_model.item(row, 2).setText(value)
        self.fits_spectrum.calibrate(m, q)
        self.fits_spectrum.plot_to(self.spectrum_plot.axes)
        
        
    def save(self):
        save_file = QFileDialog.getSaveFileName(None, "Save plot...", self.config.value('last_save_plot_dir'), "FITS file (.fit)")[0]
        if not save_file:
            return
        filename = save_file
        points = self.calibration_points()
        pixels = fits.Column(name='x_axis', format='K', array=[point['x'] for point in points])
        wavelengths = fits.Column(name='wavelength', format='D', array=[point['wavelength'] for point in points])
        cols = fits.ColDefs([pixels, wavelengths])
        tbhdu = fits.BinTableHDU.from_columns(cols)
        tbhdu.name = 'CALIBRATION_DATA'
        #self.fits_file.remove('calibration_data') #TODO: remove, or keep for history?
        self.fits_file.append(tbhdu)
        self.fits_file.writeto(filename, clobber=True)
