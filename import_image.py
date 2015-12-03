from pyui.import_image import Ui_ImportImage
from PyQt5.QtWidgets import QWidget, QToolBar, QDialog, QDialogButtonBox, QProgressDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QCoreApplication
from qmathplotwidget import QMathPlotWidget, QImPlotWidget
import matplotlib.pyplot as plt
from qtcommons import QtCommons
from pyspectrum_commons import *
import scipy.ndimage.interpolation
from pyui.rotate_image_dialog import Ui_RotateImageDialog
import os
import numpy as np
from astropy.io import fits
from object_properties_dialog import ObjectPropertiesDialog

class ImportImage(QWidget):
    def __init__(self, fits_file, settings):
        super(ImportImage, self).__init__()
        self.settings = settings
        self.fits_file = fits_file
        self.data=fits_file[0].data.astype(float)
        self.rotated = self.data
        
        self.ui = Ui_ImportImage()
        self.ui.setupUi(self)
        
        self.image_plot = QtCommons.nestWidget(self.ui.image_widget, QImPlotWidget(self.data, cmap='gray'))
        self.spatial_plot = QtCommons.nestWidget(self.ui.spatial_plot_widget, QMathPlotWidget())
        self.spectrum_plot = QtCommons.nestWidget(self.ui.spectrum_plot_widget, QMathPlotWidget())
        
        self.image_view = self.image_plot.axes_image
        
        self.toolbar = QToolBar('Image Toolbar')
        self.toolbar.addAction(QIcon(':/rotate_20'), "Rotate", lambda: self.rotate_dialog.show())
        self.toolbar.addAction(QIcon(':/save_20'), "Save", lambda: QtCommons.save_file_sticky('Save plot...', 'FITS file (.fit)', self.save, self.settings, RAW_PROFILE_DIR ))
        self.toolbar.addAction(QIcon(':/select_20'), "Select spectrum data", lambda: self.spatial_plot.add_span_selector('select_spectrum', self.spectrum_span_selected,direction='horizontal'))
        self.toolbar.addAction(QIcon.fromTheme('edit-select-invert'), "Select background data", lambda: self.spatial_plot.add_span_selector('select_background', self.background_span_selected,direction='horizontal', rectprops = dict(facecolor='blue', alpha=0.5))).setEnabled(False)
        self.toolbar.addSeparator()
        self.object_properties_dialog = ObjectPropertiesDialog()
        self.object_properties_dialog.properties_changed.connect(self.object_properties_changed)
        self.toolbar.addAction("Object properties", self.object_properties_dialog.show)
        self.max_spatial_delta = self.max_spatial_delta_angle = self.degrees = 0
        self.__init_rotate_dialog__()
        self.rotate(0)
        self.object_properties = None
        
    def object_properties_changed(self, properties):
        self.object_properties = properties
        print(self.object_properties)
        
    def background_span_selected(self, min, max):
        self.background_span_selection = (min, max)
        self.spatial_plot.add_span('background_window', min, max, 'v', facecolor='gray', alpha=0.5)
        self.image_plot.add_span('background_window', min, max, 'h', facecolor='red', alpha=0.5, clip_on=True)
        self.spatial_plot.rm_element('select_background')
        self.draw_plot(self.spectrum_plot.axes, self.spectrum_profile())
        
        
    def spectrum_span_selected(self, min, max):
        self.spectrum_span_selection = (min, max)
        self.spatial_plot.add_span('spectrum_window', min, max, 'v', facecolor='g', alpha=0.5)
        self.image_plot.add_span('spectrum_window', min, max, 'h', facecolor='y', alpha=0.5, clip_on=True)
        self.spatial_plot.rm_element('select_spectrum')
        self.draw_plot(self.spectrum_plot.axes, self.spectrum_profile())
        
    def __init_rotate_dialog__(self):
        self.rotate_dialog = QDialog()
        ui = Ui_RotateImageDialog()
        self.rotate_dialog_ui = ui
        ui.setupUi(self.rotate_dialog)
        apply_rotation = lambda: self.rotate(ui.rotate_spinbox.value())
        ui.rotate_spinbox.editingFinished.connect(apply_rotation)
        ui.rotate_spinbox.valueChanged.connect(lambda v: ui.degrees_slider.setValue(ui.rotate_spinbox.value() * 1000))
        
        ui.degrees_slider.sliderMoved.connect(lambda v: ui.rotate_spinbox.setValue(v/1000.))
        ui.degrees_slider.sliderReleased.connect(apply_rotation)
        ui.bb.button(QDialogButtonBox.Apply).clicked.connect(apply_rotation)
        ui.bb.button(QDialogButtonBox.Close).clicked.connect(lambda: self.rotate_dialog.accept())
        ui.rotate_auto.clicked.connect(self.autorotate)
        ui.rotate_mirror.clicked.connect(self.rotate_mirror)
        
    def rotate_mirror(self):
        self.rotate(self.degrees + (180. if self.degrees <= 180 else -180) )
    
    def autorotate(self):
        def get_angle(data, range):
            sum_max=(0,0)
            for deg in range:
                sum_x = scipy.ndimage.interpolation.rotate(data, deg, reshape=True, order=2, mode='constant').sum(1)
                delta = sum_x.max() - sum_x.min()
                if delta > sum_max[1]:
                    sum_max = (deg, delta)
            return sum_max[0]
        progress = QProgressDialog("Calculating best rotation angle", None, 0, 5, self);
        progress.setWindowModality(Qt.WindowModal);
        progress.show()
        
        def show_progress(progressbar, progress, angle):
            progressbar.setValue(progress)
            QCoreApplication.instance().processEvents()
            print("Step {}: {}".format(progress, round(angle, 3)))
            
        show_progress(progress, 0, 0)
            
        ratio = max(self.data.shape[0]/100, self.data.shape[1]/100)
        small = scipy.ndimage.interpolation.zoom(self.data, 1./ratio)
        
        angle = get_angle(small, np.arange(0, 180, step=0.5))
        show_progress(progress, 1, angle)
        angle = get_angle(small, np.arange(angle-3., angle+3., step=0.05))
        show_progress(progress, 2, angle)
        angle = get_angle(scipy.ndimage.interpolation.zoom(self.data, 3./ratio), np.arange(angle-2, angle+2, step=0.01))
        show_progress(progress, 3, angle)
        angle = get_angle(self.data, np.arange(angle-0.1, angle+0.1, step=0.002))
        show_progress(progress, 4, angle)
        angle = get_angle(self.data, np.arange(angle-0.01, angle+0.01, step=0.0005))
        show_progress(progress, 5, angle)
        
        angle = round(angle, 3)
        print("Step 5: {}".format(angle))
        self.rotate(angle if angle >= 0 else angle+180.)
        self.rotate_dialog.raise_()
            
        
    def rotate(self, degrees):
        self.rotate_dialog_ui.degrees_slider.setValue(degrees*1000.)
        self.rotate_dialog_ui.rotate_spinbox.setValue(degrees)
        
        if self.degrees == degrees: return
        self.degrees = degrees
        self.rotated = scipy.ndimage.interpolation.rotate(self.data, self.degrees, reshape=True, order=5, mode='constant')
        self.image_view.set_data(self.rotated)
        self.image_view.axes.relim() 
        self.image_view.axes.autoscale_view() 
        self.image_view.set_extent([self.rotated.shape[1],0, self.rotated.shape[0],0])
        self.image_view.figure.canvas.draw()
        spatial = self.spatial_profile()
        delta = spatial.max() - spatial.min()
        self.max_spatial_delta = max(delta, self.max_spatial_delta)
        self.max_spatial_delta_angle = degrees if self.max_spatial_delta == delta else self.max_spatial_delta_angle
        
        self.ui.delta_label.setText("Current rotation degrees: {:.3f}, optimal rotation angle so far: {:.3f} deg".format(self.degrees, self.max_spatial_delta_angle))
        self.draw_plot(self.spectrum_plot.axes, self.spectrum_profile())
        self.draw_plot(self.spatial_plot.axes, self.spatial_profile())
        
        
        
    def draw_plot(self, axes, data):
        axes.clear()
        axes.plot(data)
        axes.figure.tight_layout()
        axes.figure.canvas.draw()
        
    def spatial_profile(self):
        return self.rotated.sum(1)
    
    def spectrum_profile(self):
        return self.rotated[self.spectrum_span_selection[0]:self.spectrum_span_selection[1]+1,:].sum(0) if hasattr(self, 'spectrum_span_selection') else self.rotated.sum(0)
        
    def save(self, save_file):
        data = self.spectrum_profile()
        data -= np.amin(data)
        data /= np.amax(data)
        hdu = fits.PrimaryHDU(data)
        hdu.header['ORIGIN'] = 'PySpectrum'
        hdu.header['pyspec_rotated_by'] = self.degrees
        if self.object_properties:
            hdu.header['OBJECT'] = self.object_properties['name']
            hdu.header['DATE'] = self.object_properties['date'].toString(Qt.ISODate)
            hdu.header['CTYPE2'] = 'RA--TAN'
            hdu.header['CRVAL2'] = self.object_properties['ra']
            hdu.header['CTYPE3'] = 'DEC--TAN'
            hdu.header['CRVAL3'] = self.object_properties['dec']
            hdu.header['OBJTYPE'] = self.object_properties['type']
            hdu.header['SPTYPE'] = self.object_properties['sptype']
            hdu.header['OBSERVER'] = self.object_properties['observer']
            hdu.header['INSTRUMENT'] = self.object_properties['instruments'] #TODO: rename to equipment
            hdu.header['POSITION'] = self.object_properties['position']
        hdu.writeto(save_file[0], clobber=True)
    