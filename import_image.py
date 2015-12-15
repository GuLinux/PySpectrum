from pyui.import_image import Ui_ImportImage
from PyQt5.QtWidgets import QWidget, QToolBar, QDialog, QDialogButtonBox, QProgressDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QCoreApplication
from qmathplotwidget import QMathPlotWidget, QImPlotWidget
import matplotlib.pyplot as plt
from qtcommons import QtCommons
from pyspectrum_commons import *
import os
import numpy as np
from astropy.io import fits
from object_properties_dialog import ObjectPropertiesDialog
from object_properties import ObjectProperties
from rotate_image_dialog import RotateImageDialog
from project import Project

class ImportImage(QWidget):
    def icon():
        return QIcon(':/image_20')
    ACTION_TEXT = 'Import Image'
    def pick(on_ok, settings):
        open_file_sticky('Open FITS Image',FITS_IMG_EXTS, on_ok, settings, IMPORT_IMG )
    
    def __init__(self, fits_file, settings, project = None):
        super(ImportImage, self).__init__()
        self.settings = settings
        self.fits_file = fits_file
        self.project = project
        try:
            image_hdu_index = fits_file.index_of('IMAGE')
        except KeyError:
            image_hdu_index = 0
        
        original_image = fits.ImageHDU(data=fits_file[image_hdu_index].data, header=fits_file[image_hdu_index].header, name='IMAGE')
        for hdu in [h for h in self.fits_file if h.name == 'IMAGE']: self.fits_file.remove(hdu)
        self.fits_file.append(original_image)
        
        self.ui = Ui_ImportImage()
        self.ui.setupUi(self)
        
        self.rotate_dialog = RotateImageDialog(self.fits_file, image_hdu_index)
        self.rotate_dialog.rotated.connect(self.rotated)
        
        self.image_plot = QtCommons.nestWidget(self.ui.image_widget, QImPlotWidget(self.rotate_dialog.data_rotated, cmap='gray'))
        self.spatial_plot = QtCommons.nestWidget(self.ui.spatial_plot_widget, QMathPlotWidget())
        self.spectrum_plot = QtCommons.nestWidget(self.ui.spectrum_plot_widget, QMathPlotWidget())
        
        self.image_view = self.image_plot.axes_image
        
        self.toolbar = QToolBar('Image Toolbar')
        self.toolbar.addAction(QIcon(':/rotate_20'), "Rotate", lambda: self.rotate_dialog.show())
        self.toolbar.addAction(QIcon(':/save_20'), "Save", self.save_profile)
        self.toolbar.addAction(QIcon(':/select_all_20'), "Select spectrum data", lambda: self.spatial_plot.add_span_selector('select_spectrum', self.spectrum_span_selected,direction='horizontal'))
        self.toolbar.addAction(QIcon.fromTheme('edit-select-invert'), "Select background data", lambda: self.spatial_plot.add_span_selector('select_background', self.background_span_selected,direction='horizontal', rectprops = dict(facecolor='blue', alpha=0.5))).setEnabled(False)
        #self.toolbar.addAction('Stack', self.show_stack_images_dialog)
        self.toolbar.addSeparator()
        self.object_properties = ObjectProperties(self.fits_file)
        self.object_properties_dialog = ObjectPropertiesDialog(settings, self.object_properties)
        self.toolbar.addAction("Object properties", self.object_properties_dialog.show)
        self.rotated()
        
    def rotated(self):
        self.image_view.set_data(self.rotate_dialog.data_rotated)
        self.image_view.axes.relim() 
        self.image_view.axes.autoscale_view() 
        self.image_view.set_extent([self.rotate_dialog.data_rotated.shape[1],0, self.rotate_dialog.data_rotated.shape[0],0])
        self.image_view.figure.canvas.draw()
        self.draw_plot(self.spectrum_plot.axes, self.spectrum_profile())
        self.draw_plot(self.spatial_plot.axes, self.spatial_profile())
        
    def background_span_selected(self, min, max):
        self.background_span_selection = (min, max)
        self.spatial_plot.add_span('background_window', min, max, 'v', facecolor='gray', alpha=0.5)
        self.image_plot.add_span('background_window', min, max, 'h', facecolor='red', alpha=0.5, clip_on=True)
        self.draw_plot(self.spectrum_plot.axes, self.spectrum_profile())
        
        
    def spectrum_span_selected(self, min, max):
        self.spectrum_span_selection = (min, max)
        self.spatial_plot.add_span('spectrum_window', min, max, 'v', facecolor='g', alpha=0.5)
        self.image_plot.add_span('spectrum_window', min, max, 'h', facecolor='y', alpha=0.25, clip_on=True)
        self.draw_plot(self.spectrum_plot.axes, self.spectrum_profile())
        
    def draw_plot(self, axes, data):
        axes.clear()
        axes.plot(data)
        axes.figure.tight_layout()
        axes.figure.canvas.draw()
        
    def spatial_profile(self):
        return self.rotate_dialog.data_rotated.sum(1)
    
    def spectrum_profile(self):
        return self.rotate_dialog.data_rotated[self.spectrum_span_selection[0]:self.spectrum_span_selection[1]+1,:].sum(0) if hasattr(self, 'spectrum_span_selection') else self.rotate_dialog.data_rotated.sum(0)
                
    def save(self, save_file):
        print(save_file)
        data = self.spectrum_profile()
        data -= np.amin(data)
        data /= np.amax(data)
        print(self.fits_file.info())
        hdu = self.fits_file[0]
        hdu.data = data
        hdu.header['ORIGIN'] = 'PySpectrum'
        self.fits_file.writeto(save_file, clobber=True)
        
    def save_profile(self):
        if not self.project:
            save_file_sticky('Save plot...', 'FITS file (.fit)', lambda f: self.save(f[0]), self.settings, RAW_PROFILE )
            return
        if not self.object_properties.name:
            QMessageBox.information(self, 'Save FITS', 'Please set file information (name, date, etc) using the Object Properties button before saving')
            return
        file_path = self.project.add_file(Project.RAW_PROFILE, object_properties = self.object_properties, on_added=self.save)
        #self.save(file_path)
    