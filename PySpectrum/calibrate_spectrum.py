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
        self.ui.x_axis_pick.menu().addAction("Point")
        add_action = self.toolbar.addAction(QIcon.fromTheme('list-add'), 'Add calibration point')
        remove_action = self.toolbar.addAction(QIcon.fromTheme('list-remove'), 'Remove calibration point')
        save_action = self.toolbar.addAction(QIcon.fromTheme('document-save'), 'Save')
        remove_action.setEnabled(False)
        self.spectrum_plot = QtCommons.nestWidget(self.ui.spectrum_plot_widget, QMathPlotWidget())
        
        self.calibration_model = QStandardItemModel()
        self.calibration_model.setHorizontalHeaderLabels(["x-axis", "wavelength", "error"])
        self.calibration_model.rowsInserted.connect(self.calculate_calibration)
        self.calibration_model.rowsRemoved.connect(self.calculate_calibration)
        self.ui.calibration_points.setModel(self.calibration_model)
        add_action.triggered.connect(self.add_calibration_point)
        save_action.triggered.connect(self.save)
        self.ui.point_is_star.toggled.connect(lambda checked: self.ui.point_x_axis.setEnabled(not checked))
        self.fits_spectrum.plot_to(self.spectrum_plot.axes)
        
    def picked_from_range(self, type, min, max):
        point = {
            'minimum': self.fits_spectrum.data()[min:max+1].argmin() + min,
            'maximum': self.fits_spectrum.data()[min:max+1].argmax() + min,
            'central': min+(max-min)/2
            }[type]
        self.ui.point_x_axis.setValue(point)
        self.pick_selector = None
        try:
            self.pick_point_line.remove()
        except AttributeError:
            pass
        self.pick_point_line = self.spectrum_plot.axes.axvline(point, color='r')
        self.spectrum_plot.figure.canvas.draw()

    def pick_from_range(self, type):
        self.pick_selector = SpanSelector(self.spectrum_plot.axes, lambda min,max: self.picked_from_range(type, min, max), button=[1,3], direction='horizontal')

    def add_calibration_point(self):
        x_axis_item = QStandardItem("star" if self.ui.point_is_star.isChecked() else "{}".format(self.ui.point_x_axis.value()))
        x_axis_item.setData(0 if self.ui.point_is_star.isChecked() else self.ui.point_x_axis.value())
        wavelength = QStandardItem("{:.2f}".format(self.ui.point_wavelength.value()))
        wavelength.setData(self.ui.point_wavelength.value())
        self.calibration_model.appendRow([x_axis_item, wavelength, QStandardItem("n/a")])
        
    def calculate_calibration(self):
        if self.calibration_model.rowCount() < 2:
            return
        points = [{'row': row, 'x': self.calibration_model.item(row, 0).data(), 'wavelength': self.calibration_model.item(row, 1).data()} for row in range(self.calibration_model.rowCount())]
        points = sorted(points, key=lambda point: point['x'])
        m, q = np.polyfit([i['x'] for i in points], [i['wavelength'] for i in points], 1)
        f_x = lambda x: m*x+q
        for row, value in [(p['row'], "{:.2f}".format( p['wavelength']-f_x(p['x']))) for p in points]:
            self.calibration_model.item(row, 2).setText(value)
        self.fits_spectrum.calibrate(m, q)
        self.fits_spectrum.plot_to(self.spectrum_plot.axes)
        
        
    def save(self):
        save_file = QFileDialog.getSaveFileName(None, "Save plot...", self.config.value('last_save_plot_dir'), "FITS file (.fit)")[0]
        if not save_file:
            return
        filename = save_file
        self.fits_file.writeto(filename, clobber=True)