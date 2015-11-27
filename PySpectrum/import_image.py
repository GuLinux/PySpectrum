from ui_import_image import Ui_ImportImage
from PyQt5.QtWidgets import QWidget, QToolBar, QDialog, QDialogButtonBox, QFileDialog
from PyQt5.QtGui import QIcon
from qmathplotwidget import QMathPlotWidget, QImPlotWidget
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
from qtcommons import QtCommons
import scipy.ndimage.interpolation
from ui_rotate_image_dialog import Ui_RotateImageDialog
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
        self.toolbar.addAction(QIcon.fromTheme('document-save'), "Save", lambda: self.save())
        self.toolbar.addAction(QIcon.fromTheme('edit-select'), "Select spectrum data", lambda: self.spatial_plot.add_span_selector('select_spectrum', self.spectrum_span_selected,direction='horizontal', button=[1,3]))
        self.toolbar.addAction(QIcon.fromTheme('edit-select-invert'), "Select background data", lambda: self.spatial_plot.add_span_selector('select_background', self.background_span_selected,direction='horizontal', button=[1,3], rectprops = dict(facecolor='blue', alpha=0.5))).setEnabled(False)
        self.max_spatial_delta = self.max_spatial_delta_angle = 0
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
        ui.bb.button(QDialogButtonBox.Apply).clicked.connect(lambda: self.rotate(ui.rotate_spinbox.value()))
        ui.bb.button(QDialogButtonBox.Close).clicked.connect(lambda: self.rotate_dialog.accept())
        
    def rotate(self, degrees):
        self.degrees = degrees
        self.rotated = scipy.ndimage.interpolation.rotate(self.data, self.degrees, mode='nearest')
        self.image_view.set_data(self.rotated)
        self.image_view.figure.canvas.draw()
        spatial = self.spatial_profile()
        delta = spatial.max() - spatial.min()
        self.max_spatial_delta = max(delta, self.max_spatial_delta)
        self.max_spatial_delta_angle = degrees if self.max_spatial_delta == delta else self.max_spatial_delta_angle
        
        self.ui.delta_label.setText("Delta: {:.2f}, max: {:.2f} at {:.2f} deg".format(delta, self.max_spatial_delta, self.max_spatial_delta_angle))
        self.draw_plot(self.spectrum_plot.axes, self.spectrum_profile())
        self.draw_plot(self.spatial_plot.axes, self.spatial_profile())
        
        
    def draw_plot(self, axes, data):
        axes.clear()
        axes.plot(data)
        axes.figure.canvas.draw()
        
    def spatial_profile(self):
        return self.rotated.sum(1)
    
    def spectrum_profile(self):
        return self.rotated[self.spectrum_span_selection[0]:self.spectrum_span_selection[1]+1,:].sum(0) if hasattr(self, 'spectrum_span_selection') else self.rotated.sum(0)
        
    #TODO: Move?
    def save(self):
        save_file = QFileDialog.getSaveFileName(None, "Save plot...", self.config.value('last_plot_save_dir'), "FITS file (.fit)")[0]
        if not save_file:
            return
        self.config.setValue('last_plot_save_dir', os.path.dirname(os.path.realpath(save_file)))
        data = self.spectrum_profile()
        data -= np.amin(data)
        data /= np.amax(data)
        hdu = fits.PrimaryHDU(data)
        hdu.header['pyspec_rotated_by'] = self.degrees
        hdu.writeto(save_file, clobber=True)
    