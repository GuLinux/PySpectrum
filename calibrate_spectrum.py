from ui_calibrate_spectrum import Ui_CalibrateSpectrum
from PyQt5.QtWidgets import QWidget, QToolBar, QDialog, QDialogButtonBox, QFileDialog, QMenu, QAction, QInputDialog
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
from scipy.interpolate import *

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
        self.ui.wavelength_pick.clicked.connect(self.pick_wavelength)
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
        self.ui.set_dispersion.clicked.connect(self.calibrate_with_dispersion)
        save_action.triggered.connect(self.save)
        self.ui.point_is_star.toggled.connect(lambda checked: self.ui.wavelength_pick.setEnabled(not checked))
        self.ui.point_is_star.toggled.connect(lambda checked: self.ui.point_wavelength.setEnabled(not checked))
        self.fits_spectrum.plot_to(self.spectrum_plot.axes)

        hdu_calibration_points = [h for h in self.fits_file if h.name == 'CALIBRATION_DATA']
        if len(hdu_calibration_points) > 0:                
            for point in hdu_calibration_points[-1].data:
                self.add_calibration_point_data(point[0], point[1])
        self.calculate_calibration()
    
    def open_reference(self, file):
        fits_spectrum = FitsSpectrum(fits.open(file))
        data = fits_spectrum.data()
        data /= data.max()
        line = Line2D(fits_spectrum.x_axis(), data, color='gray')
        self.spectrum_plot.axes.add_line(line)
        self.spectrum_plot.figure.canvas.draw()
        
    def picked_from_range(self, type, min, max):
        min=(self.fits_spectrum.x_uncalibrated(min))
        max=(self.fits_spectrum.x_uncalibrated(max))
        point = {
            'minimum': self.fits_spectrum.data()[min:max+1].argmin() + min,
            'maximum': self.fits_spectrum.data()[min:max+1].argmax() + min,
            'central': min+(max-min)/2
            }[type]
        if type != 'central':
            subplot = QMathPlotWidget()
            y_axis = self.fits_spectrum.data()[min:max+1]
            x_axis = np.arange(min, min+len(y_axis))
            spline = UnivariateSpline(x_axis, y_axis, k=2)
            interp = interp1d(x_axis, y_axis, kind='cubic')
            subplot.axes.plot(x_axis, y_axis, 'o', x_axis, spline(x_axis), '-', x_axis, interp(x_axis), '--')
            subplot.show()
            
        self.ui.point_x_axis.setValue(point)
        self.spectrum_plot.rm_element('pick_x_axis')
        self.ui.point_wavelength.setValue(self.fits_spectrum.x_calibrated(point))
        self.spectrum_plot.add_line("x_axis_pick", self.fits_spectrum.x_calibrated(point), color='r')

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
        
    def pick_wavelength(self):
        # TODO: add a full database of spectral lines
        wavelengths = [
            ('Balmer H-α', 6563),
            ('Balmer H-β', 4861),
            ('Balmer H-γ', 4341),
            ('Balmer H-δ', 4102),
            ('Balmer H-ε', 3970),
            ('Balmer H-ζ', 3889),
            ('Balmer H-η', 3835),
            ]
        wavelength_choice = QInputDialog.getItem(None, 'Choose wavelength', 'Pick a wavelength from the list below: ', [wavelength[0] for wavelength in wavelengths], 0, False)
        if not wavelength_choice[1]:
            return
        wavelength = [wavelength[1] for wavelength in wavelengths if wavelength[0] == wavelength_choice[0]][0]
        self.ui.point_wavelength.setValue(wavelength)
    
    def add_calibration_point(self):
        self.add_calibration_point_data(self.ui.point_x_axis.value(), 0 if self.ui.point_is_star.isChecked() else self.ui.point_wavelength.value())

    def calibration_points(self):
        return [{'row': row, 'x': self.calibration_model.item(row, 0).data(), 'wavelength': self.calibration_model.item(row, 1).data()} for row in range(self.calibration_model.rowCount())]
    
    def calibrate_with_dispersion(self):
        self.fits_spectrum.dispersion = self.ui.dispersion.value()
        self.calculate_calibration()

    def calculate_calibration(self):
        points_number = self.calibration_model.rowCount()
        self.ui.set_dispersion.setEnabled(points_number <= 1)
        self.ui.dispersion.setEnabled(points_number <= 1)
        
        if points_number == 0:
            self.fits_spectrum.reset()
        else:
            points = sorted(self.calibration_points(), key=lambda point: point['x'])
            self.fits_spectrum.calibrate(points)
            for row, value in [(p['row'], "{:.2f}".format( p['wavelength']-self.fits_spectrum.x_calibrated(p['x']))) for p in points]:
                self.calibration_model.item(row, 2).setText(value)
            
        self.ui.dispersion.setValue(self.fits_spectrum.dispersion)
        self.fits_spectrum.plot_to(self.spectrum_plot.axes)
        
        
    def save(self):
        save_file = QFileDialog.getSaveFileName(None, "Save plot...", self.config.value('last_save_plot_dir'), "FITS file (.fit)")[0]
        if not save_file:
            return
        self.fits_spectrum.save(save_file, self.calibration_points())
