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
        
        image_plot = QtCommons.nestWidget(self.ui.image_widget, QImPlotWidget(self.data, cmap='gray'))
        self.spatial_plot = QtCommons.nestWidget(self.ui.spatial_plot_widget, QMathPlotWidget())
        self.spectrum_plot = QtCommons.nestWidget(self.ui.spectrum_plot_widget, QMathPlotWidget())
        
        self.image_view = image_plot.axes_image
        
        self.toolbar = QToolBar('Image Toolbar')
        self.toolbar.addAction(QIcon.fromTheme('transform-rotate'), "Rotate", lambda: self.rotate_dialog.show())
        self.toolbar.addAction(QIcon.fromTheme('document-save'), "Save", lambda: self.save())
        self.toolbar.addAction(QIcon.fromTheme('edit-select'), "Select spectrum data", self.spectrum_span_select)
        self.max_spatial_delta = self.max_spatial_delta_angle = 0
        self.rotate(0)
        self.__init_rotate_dialog__()
        
    def spectrum_span_select(self):
        self.select_spectrum_span = SpanSelector(self.spatial_plot.axes, self.spectrum_span_selected, button=[1,3], direction='horizontal')
        
    def spectrum_span_selected(self, min, max):
        print("min={}, max={}".format(min,max))
        try:
            self.spectrum_span_selection[2].remove()
        except AttributeError:
            pass
        self.spectrum_span_selection = (min, max, self.spatial_plot.axes.axvspan(min, max, facecolor='0.5', alpha=0.5))
        self.spatial_plot.figure.canvas.draw()
        self.select_spectrum_span = None
        
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
        spatial = self.calc_data(1)
        delta = spatial.max() - spatial.min()
        self.max_spatial_delta = max(delta, self.max_spatial_delta)
        self.max_spatial_delta_angle = degrees if self.max_spatial_delta == delta else self.max_spatial_delta_angle
        
        self.ui.delta_label.setText("Delta: {:.2f}, max: {:.2f} at {:.2f} deg".format(delta, self.max_spatial_delta, self.max_spatial_delta_angle))
        self.draw_plot(self.spectrum_plot.axes, 0)
        self.draw_plot(self.spatial_plot.axes, 1)
        
        
    def draw_plot(self, axes, direction):
        axes.clear()
        axes.plot(self.calc_data(direction))
        axes.figure.canvas.draw()
        
    def calc_data(self, direction):
        return (self.rotated - 0).sum(direction)
    
    #TODO: Move?
    def save(self):
        save_file = QFileDialog.getSaveFileName(None, "Save plot...", self.config.value('last_plot_save_dir'), "FITS file (.fit)")[0]
        if not save_file:
            return
        self.config.setValue('last_plot_save_dir', os.path.dirname(os.path.realpath(save_file)))
        data = self.calc_data(0)
        data -= np.amin(data)
        data /= np.amax(data)
        hdu = fits.PrimaryHDU(data)
        hdu.header['pyspec_rotated_by'] = self.degrees
        hdu.writeto(save_file, clobber=True)
    