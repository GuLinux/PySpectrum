from pyui.rotate_image_dialog import Ui_RotateImageDialog
from PyQt5.QtWidgets import QWidget, QDialog, QDialogButtonBox, QProgressDialog, QApplication
import scipy.ndimage.interpolation
from PyQt5.QtCore import Qt, pyqtSignal
import numpy as np
import time

class RotateImageDialog(QDialog):
    rotated = pyqtSignal()
    
    def __init__(self, fits_file, image_hdu_index = 0):
        QDialog.__init__(self)
        self.image_hdu_index = image_hdu_index
        self.fits_file = fits_file
        self.max_spatial_delta = self.max_spatial_delta_angle = 0
        self.data=fits_file[image_hdu_index].data.astype(float)
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
        self.rotate(self.degrees(), force=True)
        
    def rotate_mirror(self):
        self.rotate(self.degrees() + (180. if self.degrees() <= 180 else -180) )
    
    def autorotate(self):
        def get_angle(data, range):
            start = time.time()
            sum_max=(0,0)
            for deg in range:
                sum_x = scipy.ndimage.interpolation.rotate(data, deg, reshape=True, order=2, mode='constant').sum(1)
                delta = sum_x.max() - sum_x.min()
                if delta > sum_max[1]:
                    sum_max = (deg, delta)
            print("elapsed: {}".format(time.time() - start))
            return sum_max[0]
        
        progress = QProgressDialog("Calculating best rotation angle", None, 0, 5, self);
        progress.setWindowModality(Qt.WindowModal);
        progress.show()
        
        def show_progress(progressbar, progress, angle):
            progressbar.setValue(progress)
            QApplication.instance().processEvents()
            print("Step {}: {}".format(progress, round(angle, 3)))
            
        show_progress(progress, 0, 0)
            
        ratio = max(self.data.shape[0]/100, self.data.shape[1]/100)
        
        data = self.fits_file[self.image_hdu_index].data
        small = scipy.ndimage.interpolation.zoom(data, 1./ratio)
        
        angle = get_angle(small, np.arange(0, 180, step=0.5))
        show_progress(progress, 1, angle)
        angle = get_angle(small, np.arange(angle-4., angle+4., step=0.01))
        show_progress(progress, 2, angle)
        angle = get_angle(scipy.ndimage.interpolation.zoom(data, 2./ratio) if 2./ratio < 1 else data, np.arange(angle-2, angle+2, step=0.005))
        show_progress(progress, 3, angle)
        angle = get_angle(scipy.ndimage.interpolation.zoom(data, 4/ratio) if 4/ratio < 1 else data, np.arange(angle-0.5, angle+0.5, step=0.001))
        show_progress(progress, 4, angle)
        angle = get_angle(self.data, np.arange(angle-0.03, angle+0.03, step=0.0005))
        show_progress(progress, 5, angle)
        
        angle = round(angle, 3)
        print("Step 5: {}".format(angle))
        self.rotate(angle if angle >= 0 else angle+180.)
        self.raise_()
            
        
    def rotate(self, degrees, force = False):
        self.ui.degrees_slider.setValue(degrees*1000.)
        self.ui.rotate_spinbox.setValue(degrees)
        
        if self.degrees() == degrees and not force: return
        self.fits_file[0].header.set('pyspec_rotated_by', value = degrees, comment='Image rotation angle, degrees')
        self.data_rotated = scipy.ndimage.interpolation.rotate(self.data, degrees, reshape=True, order=5, mode='constant')
        
        spatial = self.data_rotated.sum(1)
        delta = spatial.max() - spatial.min()
        self.max_spatial_delta = max(delta, self.max_spatial_delta)
        
        self.max_spatial_delta_angle = degrees if self.max_spatial_delta == delta else self.max_spatial_delta_angle
        self.ui.rotation_info.setText("Current rotation degrees: {:.3f}, optimal rotation angle so far: {:.3f} deg".format(degrees, self.max_spatial_delta_angle))
        
        self.rotated.emit()
        
        
    def degrees(self):
        return self.fits_file[0].header.get('pyspec_rotated_by', 0)