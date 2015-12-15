from pyui.calibrate_spectrum import Ui_CalibrateSpectrum
from PyQt5.QtWidgets import QWidget, QToolBar, QDialog, QDialogButtonBox, QFileDialog, QMenu, QAction, QInputDialog
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QByteArray, QTimer
from qmathplotwidget import QMathPlotWidget
import matplotlib.pyplot as plt
from qtcommons import QtCommons
from pyui.rotate_image_dialog import Ui_RotateImageDialog
import os
import numpy as np
from astropy.io import fits
from fits_spectrum import FitsSpectrum
from matplotlib.widgets import SpanSelector
from matplotlib.lines import Line2D
from reference_spectra_dialog import ReferenceSpectraDialog
from scipy.interpolate import *
from pyui.select_plotted_point import Ui_SelectPlottedPoints
from pyspectrum_commons import *
from lines_dialog import LinesDialog
from object_properties import ObjectProperties
from object_properties_dialog import ObjectPropertiesDialog
from project import Project

class SelectPlottedPoints(QDialog):
    point = pyqtSignal(int)

    def __init__(self, data, min, max, settings, type):
        super(SelectPlottedPoints, self).__init__()
        self.ui = Ui_SelectPlottedPoints()
        self.ui.setupUi(self)
        self.type = type
        self.min = min
        self.y_axis = data[min:max]
        self.x_axis = np.arange(min, min+len(self.y_axis))
        self.ui.x_coordinate.setRange(self.x_axis[0], self.x_axis[-1])
        self.plot = QtCommons.nestWidget(self.ui.plot_widget, QMathPlotWidget())
        self.finished.connect(lambda: self.deleteLater())
        self.ui.smoothing_factor.valueChanged.connect(self.factor_valueChanged)
        self.ui.smoothing_degree.valueChanged.connect(lambda v: self.draw())
        self.ui.smoothing_factor_auto.toggled.connect(lambda v: self.draw())
        self.ui.smoothing_factor_auto.toggled.connect(lambda v: self.ui.smoothing_factor.setEnabled(not v))
        self.restoreGeometry(settings.value('select_plotted_points_geometry', QByteArray()))
        self.finished.connect(lambda: settings.setValue('select_plotted_points_geometry', self.saveGeometry()))
        self.ui.x_coordinate.valueChanged.connect(self.set_point)
        
        QTimer.singleShot(100, self.draw)

    @pyqtSlot(float)
    def factor_valueChanged(self, f):
        self.draw()
        
    def draw(self):
        self.ui.smoothing_degree_value.setText("{}".format(self.ui.smoothing_degree.value()))
        smoothing_factor = self.ui.smoothing_factor.value() if not self.ui.smoothing_factor_auto.isChecked() else None
        spline = UnivariateSpline(self.x_axis, self.y_axis, k=self.ui.smoothing_degree.value(), s=smoothing_factor)
        f_x = spline(self.x_axis)
        self.plot.axes.plot(self.x_axis, self.y_axis, 'o', self.x_axis, f_x, '-')
        value = (f_x.argmin() if self.type == 'minimum' else f_x.argmax()) + self.min
        self.ui.x_coordinate.setValue(value)
        self.set_point(value)
        
    @pyqtSlot(int)
    def set_point(self, point):
        self.x_point = point
        self.point.emit(point)
        self.plot.add_line("x_axis_pick", point, color='r')
        self.plot.figure.canvas.draw()

class CalibrateSpectrum(QWidget):
    def __init__(self, fits_file, settings, database, project=None):
        super(CalibrateSpectrum, self).__init__()
        self.project=project
        self.settings = settings
        self.fits_spectrum = FitsSpectrum(fits_file)
        self.fits_spectrum.spectrum.normalize_to_max()
        self.fits_file = fits_file
        self.ui = Ui_CalibrateSpectrum()
        self.ui.setupUi(self)
        self.toolbar = QToolBar('Calibration Toolbar')
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.ui.x_axis_pick.setMenu(QMenu())
        self.ui.x_axis_pick.menu().addAction("Maximum from range").triggered.connect(lambda: self.pick_from_range('maximum'))
        self.ui.x_axis_pick.menu().addAction("Minimum from range").triggered.connect(lambda: self.pick_from_range('minimum'))
        self.ui.x_axis_pick.menu().addAction("Central value from range").triggered.connect(lambda: self.pick_from_range('central'))
        self.ui.wavelength_pick.clicked.connect(lambda: self.lines_dialog.show())
        
        save_action = self.toolbar.addAction(QIcon(':/save_20'), 'Save', self.save_spectrum)
        self.spectrum_plot = QtCommons.nestWidget(self.ui.spectrum_plot_widget, QMathPlotWidget())
        
        self.reference_spectra_dialog = ReferenceSpectraDialog(database)
        self.reference_spectra_dialog.setup_menu(self.toolbar, self.spectrum_plot.axes, settings)

        self.object_properties = ObjectProperties(self.fits_file, project=project)
        self.object_properties_dialog = ObjectPropertiesDialog(settings, self.object_properties)
        self.toolbar.addAction("Object properties", self.object_properties_dialog.show)

        self.calibration_model = QStandardItemModel()
        self.calibration_model.setHorizontalHeaderLabels(["x-axis", "wavelength", "error"])
        self.ui.calibration_points.setModel(self.calibration_model)
        self.ui.calibration_points.selectionModel().selectionChanged.connect(lambda selected, deselected: self.ui.remove_calibration_point.setEnabled(len(selected.indexes()) > 0)  )
        self.ui.add_calibration_point.clicked.connect(self.add_calibration_point)
        self.ui.remove_calibration_point.setEnabled(False)
        self.ui.remove_calibration_point.clicked.connect(self.remove_calibration_point)
        if project and project.avg_dispersion():
            self.ui.set_dispersion.setMenu(QMenu())
            self.ui.set_dispersion.menu().addAction('From input value', self.calculate_calibration)
            self.ui.set_dispersion.menu().addAction('From Project', lambda: self.calculate_calibration(project.avg_dispersion()))
        else:
            self.ui.set_dispersion.clicked.connect(self.calculate_calibration)
        self.ui.point_is_star.toggled.connect(lambda checked: self.ui.wavelength_pick.setEnabled(not checked))
        self.ui.point_is_star.toggled.connect(lambda checked: self.ui.point_wavelength.setEnabled(not checked))
        self.fits_spectrum.plot_to(self.spectrum_plot.axes)
        
        self.toolbar.addSeparator()
        self.toolbar.addAction("Zoom", self.spectrum_plot.select_zoom)
        self.toolbar.addAction("Reset Zoom", lambda: self.spectrum_plot.reset_zoom(self.fits_spectrum.spectrum.wavelengths, self.fits_spectrum.spectrum.fluxes.min(), self.fits_spectrum.spectrum.fluxes.max()))
        self.toolbar.addSeparator()
        
        self.lines_dialog = LinesDialog(database, settings, self.spectrum_plot, enable_picker = False, selection_mode = 'single')
        self.lines_dialog.lines.connect(self.picked_line)

        hdu_calibration_points = [h for h in self.fits_file if h.name == FitsSpectrum.CALIBRATION_DATA]
        if len(hdu_calibration_points) > 0:                
            for point in hdu_calibration_points[-1].data:
                self.add_calibration_point_data(point[0], point[1])
        self.calculate_calibration()
    
  
    def picked_from_range(self, type, min, max):
        min=(self.fits_spectrum.spectrum.wavelength_index(min))
        max=(self.fits_spectrum.spectrum.wavelength_index(max))
        add_line = lambda x: self.spectrum_plot.add_line("x_axis_pick", self.fits_spectrum.spectrum.wavelengths[x], color='r')
        set_x_value = lambda x: self.ui.point_x_axis.setValue(x)

        if type != 'central':
            subplot = SelectPlottedPoints(self.fits_spectrum.spectrum.fluxes, min, max+1, self.settings, type)
            subplot.point.connect(add_line)
            subplot.point.connect(set_x_value)
            subplot.show()
            return
        point = min+(max-min)/2
        self.ui.point_x_axis.setValue(point)
        set_x_value(point)
        add_line(point)

    def pick_from_range(self, type):
        self.spectrum_plot.add_span_selector('pick_x_axis', lambda min,max: self.picked_from_range(type, min, max),direction='horizontal')

    def remove_calibration_point(self):
        self.calibration_model.removeRow(self.ui.calibration_points.selectionModel().selectedIndexes()[0].row())
        self.calculate_calibration()
    
    def add_calibration_point_data(self, x_value, wavelength):
        x_axis_item = QStandardItem("star" if x_value == 0 else "{}".format(x_value))
        x_axis_item.setData(x_value)
        wavelength_item = QStandardItem("{:.2f}".format(wavelength))
        wavelength_item.setData(wavelength)
        self.calibration_model.appendRow([x_axis_item, wavelength_item, QStandardItem("n/a")])
        self.spectrum_plot.rm_element('x_axis_pick')
        
    def picked_line(self, lines):
        self.ui.point_wavelength.setValue(lines[0]['lambda'])
    
    def add_calibration_point(self):
        self.add_calibration_point_data(self.ui.point_x_axis.value(), 0 if self.ui.point_is_star.isChecked() else self.ui.point_wavelength.value())
        self.calculate_calibration()
        
    def calibration_points(self):
        return [{'row': row, 'x': self.calibration_model.item(row, 0).data(), 'wavelength': self.calibration_model.item(row, 1).data()} for row in range(self.calibration_model.rowCount())]
    

    def calculate_calibration(self, dispersion = None):
        points_number = self.calibration_model.rowCount()
        print(points_number)
        self.ui.set_dispersion.setEnabled(points_number == 1)
        self.ui.dispersion.setEnabled(points_number == 1)
        
        if points_number == 0:
            self.fits_spectrum.reset()
            self.lines_dialog.set_picker_enabled(False)
        else:
            self.lines_dialog.set_picker_enabled(True)
            points = sorted(self.calibration_points(), key=lambda point: point['x'])
            self.fits_spectrum.calibrate(points, dispersion if dispersion else self.ui.dispersion.value() )
            for row, value in [(p['row'], "{:.2f}".format( p['wavelength']-self.fits_spectrum.spectrum.wavelengths[p['x']])) for p in points]:
                self.calibration_model.item(row, 2).setText(value)
            
        self.ui.dispersion.setValue(self.fits_spectrum.spectrum.dispersion())
        self.fits_spectrum.plot_to(self.spectrum_plot.axes)
        
    def save_spectrum(self):
        if not self.project:
            save_file_sticky('Save plot...', 'FITS file (.fit)', lambda f: self.save(f[0]), self.settings, CALIBRATED_PROFILE, [RAW_PROFILE])
            return
        self.project.add_file(Project.CALIBRATED_PROFILE, object_properties = self.object_properties, on_added=self.save)
        
    def save(self, filename):
        self.fits_spectrum.save(filename, self.calibration_points())
