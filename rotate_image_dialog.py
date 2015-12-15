from pyui.rotate_image_dialog import Ui_RotateImageDialog
from PyQt5.QtWidgets import QWidget, QDialog, QDialogButtonBox, QProgressDialog, QApplication
import scipy.ndimage.interpolation
from scipy.interpolate import UnivariateSpline
from PyQt5.QtCore import Qt, pyqtSignal
import numpy as np
import time
from fits_spectrum import *
from qmathplotwidget import *
from scipy.optimize import *
class RotateImageDialog(QDialog):
    rotated = pyqtSignal()
    
    def __init__(self, fits_file, image_hdu_index = 0, project = None):
        QDialog.__init__(self)
        self.image_hdu_index = image_hdu_index
        self.fits_file = fits_file
        self.max_spatial_delta = self.max_spatial_delta_angle = 0
        self.data=fits_file[image_hdu_index].data.astype(float)
        self.background = np.median(self.data)
        #self.background = np.median([d for d in np.array(self.data).flatten() if d <= self.background])
        self.data_rotated = self.data
        self.ui = Ui_RotateImageDialog()
        self.ui.setupUi(self)
        apply_rotation = lambda: self.rotate(self.ui.rotate_spinbox.value())
        self.ui.rotate_spinbox.editingFinished.connect(apply_rotation)
        self.ui.rotate_spinbox.valueChanged.connect(lambda v: self.ui.degrees_slider.setValue(self.ui.rotate_spinbox.value() * 1000))
        
        self.ui.degrees_slider.sliderMoved.connect(lambda v: self.ui.rotate_spinbox.setValue(v/1000.))
        self.ui.degrees_slider.sliderReleased.connect(apply_rotation)
        self.ui.bb.button(QDialogButtonBox.Apply).clicked.connect(apply_rotation)
        self.ui.bb.button(QDialogButtonBox.Close).clicked.connect(lambda: self.accept())
        self.ui.rotate_auto.clicked.connect(self.autorotate)
        self.ui.rotate_mirror.clicked.connect(self.rotate_mirror)
        self.rotate(project.rotation_degrees() if project and project.rotation_degrees() else self.degrees(), force=True)
        
    def rotate_mirror(self):
        self.rotate(self.degrees() + (180. if self.degrees() <= 180 else -180) )
    
    def autorotate(self):
        _rotate = lambda data, d, order=3: scipy.ndimage.interpolation.rotate(data, d, reshape=True, order=order, mode='constant', cval = self.background)
        def get_angle(data, min, max, xtol=1e-10):
            start = time.time()
            get_data = lambda d: self.__fwhm(_rotate(data, d), ypos=0.25)[0]
            result = minimize_scalar(get_data, bracket=[min,max], method='brent', options={'xtol': xtol})
            print(result)
            print(result.x)
            print("elapsed: {}".format(time.time() - start))
            return result.x
        
        progress = QProgressDialog("Calculating best rotation angle", None, 0, 4, self);
        progress.setWindowModality(Qt.WindowModal);
        progress.show()
        
        def show_progress(progressbar, progress, angle):
            progressbar.setValue(progress)
            QApplication.instance().processEvents()
            print("Step {}: {}".format(progress, round(angle, 5)))
            
        show_progress(progress, 0, 0)
            
        ratio = max(self.data.shape[0]/100, self.data.shape[1]/100)
        
        data = self.fits_file[self.image_hdu_index].data
        small = scipy.ndimage.interpolation.zoom(data, 1./ratio)
        
        angle = get_angle(small, 0, 180)
        show_progress(progress, 1, angle)
        #angle = get_angle(small, np.arange(angle-4., angle+4., step=0.01))
        #show_progress(progress, 2, angle)
        angle = get_angle(scipy.ndimage.interpolation.zoom(data, 2./ratio) if 2./ratio < 1 else data, angle-2, angle+2)
        show_progress(progress, 2, angle)
        angle = get_angle(scipy.ndimage.interpolation.zoom(data, 3/ratio) if 3/ratio < 1 else data, angle-1, angle+1)
        show_progress(progress, 3, angle)
        angle = get_angle(self.data, angle-0.0002, angle+0.0002)
        show_progress(progress, 4, angle)
        
        angle = round(angle, 5)
        angle = angle if angle > 0 else angle + 360.
        progress.accept()
        print("Step 5: {}".format(angle))
        self.rotate(angle)
        self.raise_()
            
            
    def __fwhm(self, data, ypos=0.5):
        spatial = data.sum(1)
        spatial = spatial-np.min(spatial)
        spatial_range = range(0, len(spatial))
        spline = UnivariateSpline(spatial_range, (spatial -np.max(spatial)*ypos), s=0.1, k=3)
        roots = spline.roots()
        if len(roots) < 2:
            return np.inf
        return roots[-1]-roots[0], roots

        
    def rotate(self, degrees, force = False):
        self.ui.degrees_slider.setValue(degrees*1000.)
        self.ui.rotate_spinbox.setValue(degrees)
        
        if self.degrees() == degrees and not force: return
        self.fits_file[0].header.set(FitsSpectrum.ROTATION, value = degrees, comment='Image rotation angle, degrees')
        self.data_rotated = scipy.ndimage.interpolation.rotate(self.data, degrees, reshape=True, order=5, mode='constant', cval = self.background)
        print("fwhm: {}".format(self.__fwhm(self.data_rotated)))
        spatial = self.data_rotated.sum(1)
        delta = spatial.max() - spatial.min()
        self.max_spatial_delta = max(delta, self.max_spatial_delta)
        self.max_spatial_delta_angle = degrees if self.max_spatial_delta == delta else self.max_spatial_delta_angle
        self.ui.rotation_info.setText("Current rotation degrees: {:.3f}, optimal rotation angle so far: {:.3f} deg".format(degrees, self.max_spatial_delta_angle))
        
        self.rotated.emit()
        
        
    def degrees(self):
        return self.fits_file[0].header.get(FitsSpectrum.ROTATION, 0)