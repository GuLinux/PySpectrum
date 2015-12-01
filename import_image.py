from pyui.import_image import Ui_ImportImage
from PyQt5.QtWidgets import QWidget, QToolBar, QDialog, QDialogButtonBox
from PyQt5.QtGui import QIcon
from qmathplotwidget import QMathPlotWidget, QImPlotWidget
import matplotlib.pyplot as plt
from qtcommons import QtCommons
import scipy.ndimage.interpolation
from pyui.rotate_image_dialog import Ui_RotateImageDialog
import os
import numpy as np
from astropy.io import fits

class ImportImage(QWidget):
    def __init__(self, fits_file, config):
        super(ImportImage, self).__init__()
        self.config = config
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
        self.toolbar.addAction(QIcon.fromTheme('transform-rotate'), "Rotate", lambda: self.rotate_dialog.show())
        self.toolbar.addAction(QIcon.fromTheme('document-save'), "Save", lambda: QtCommons.save_file('Save plot...', 'FITS file (.fit)', self.save, self.config.value('last_plot_save_dir')))
        self.toolbar.addAction(QIcon.fromTheme('edit-select'), "Select spectrum data", lambda: self.spatial_plot.add_span_selector('select_spectrum', self.spectrum_span_selected,direction='horizontal'))
        self.toolbar.addAction(QIcon.fromTheme('edit-select-invert'), "Select background data", lambda: self.spatial_plot.add_span_selector('select_background', self.background_span_selected,direction='horizontal', rectprops = dict(facecolor='blue', alpha=0.5))).setEnabled(False)
        self.max_spatial_delta = self.max_spatial_delta_angle = self.degrees = 0
        self.rotate(0)
        self.__init_rotate_dialog__()
        
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
        ui.setupUi(self.rotate_dialog)
        apply_rotation = lambda: self.rotate(ui.rotate_spinbox.value())
        ui.rotate_spinbox.editingFinished.connect(apply_rotation)
        ui.rotate_spinbox.valueChanged.connect(lambda v: ui.degrees_slider.setValue(ui.rotate_spinbox.value() * 1000))
        
        ui.degrees_slider.sliderMoved.connect(lambda v: ui.rotate_spinbox.setValue(v/1000.))
        ui.degrees_slider.sliderReleased.connect(apply_rotation)
        ui.bb.button(QDialogButtonBox.Apply).clicked.connect(apply_rotation)
        ui.bb.button(QDialogButtonBox.Close).clicked.connect(lambda: self.rotate_dialog.accept())
        
    def rotate(self, degrees):
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
        
        self.ui.delta_label.setText("Delta: {:.3f}, max: {:.3f} at {:.3f} deg".format(delta, self.max_spatial_delta, self.max_spatial_delta_angle))
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
        self.config.setValue('last_plot_save_dir', os.path.dirname(os.path.realpath(save_file[0])))
        data = self.spectrum_profile()
        data -= np.amin(data)
        data /= np.amax(data)
        hdu = fits.PrimaryHDU(data)
        hdu.header['pyspec_rotated_by'] = self.degrees
        hdu.writeto(save_file[0], clobber=True)
    