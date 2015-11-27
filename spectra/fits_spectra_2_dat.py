#!/bin/python
import astropy
from astropy.io import fits
import sys
import numpy as np

import matplotlib.pyplot as plt
import time
import scipy.ndimage.interpolation
from matplotlib.widgets import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSettings
import os

class DisplayImage:
    
  def __init_rotate_dialog__(self):
    self.rotate_dialog = QDialog()
    self.rotate_dialog.windowTitle = "Rotate Image"
    rotate_layout = QGridLayout()
    self.rotate_dialog.setLayout(rotate_layout)
    rotate_spinbox = QDoubleSpinBox()
    rotate_spinbox.setRange(0, 360)
    rotate_spinbox.setSingleStep(0.1)
    rotate_spinbox.setDecimals(2)
    rotate_layout.addWidget(QLabel("Enter degrees for image rotation"))
    rotate_layout.addWidget(rotate_spinbox)
    bb = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Close)
    bb.button(QDialogButtonBox.Apply).clicked.connect(lambda: self.rotate(rotate_spinbox.value()))
    bb.button(QDialogButtonBox.Close).clicked.connect(lambda: self.rotate_dialog.accept())
    rotate_layout.addWidget(bb)
    

    
  def __init__(self, image):
    self.config = QSettings('GuLinux', 'PySpectra')
    self.__init_rotate_dialog__()
    self.original = image.astype(float)
    self.rotated = self.original
    self.background = np.zeros((1,1), float)
    self.image_view = plt.imshow(self.original, cmap='gray')
    self.brotate = Button(self.image_view.figure.add_axes([0, 0.95, 0.1, 0.05]), "Rotate")
    self.bselect_background = Button(self.image_view.figure.add_axes([0.1, 0.95, 0.25, 0.05]), "Select Background")
    self.bsave = Button(self.image_view.figure.add_axes([0.1 + 0.25, 0.95, 0.1, 0.05]), "Save")
    self.brotate.on_clicked(lambda ev: self.rotate_dialog.show())
    self.bsave.on_clicked(self.save)
    self.bselect_background.on_clicked(self.select_bg)
    self.RS = RectangleSelector(self.image_view.axes, self.bg_selected,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
    
    plt.figure()
    self.image_plot = plt.axes()
    self.degrees = 0
    self.draw_plot()
    plt.show()
    
  def bg_selected(self, eclick, erelease):
    print(eclick, erelease)
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    self.background = self.rotated[x1:x2, y1:y2]
    print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    print("mean background: %f" % self.background.mean())
    self.RS.set_active(False)
    self.draw_plot()
    
  def calc_data(self):
    return (self.rotated - self.background.mean()).sum(0)
    
  def draw_plot(self):
    self.image_plot.clear()
    self.image_plot.plot(self.calc_data())
    self.image_plot.figure.canvas.draw()
    
  def select_bg(self, evt):
    self.RS.set_active(True)
    
  def rotate(self, degrees):
    self.degrees = degrees
    self.rotated = scipy.ndimage.interpolation.rotate(self.original, self.degrees)
    self.image_view.set_data(self.rotated)
    self.image_view.figure.canvas.draw()
    self.draw_plot()
    
  def save(self, ev):
    save_file = QFileDialog.getSaveFileName(None, "Save plot...", self.config.value('last_plot_save_dir'), "FITS file (.fit)")
    if not save_file[0]:
      return
    filename = save_file[0]
    self.config.setValue('last_plot_save_dir', os.path.dirname(os.path.realpath(filename)))
    data = self.calc_data()
    data -= np.amin(data)
    data /= np.amax(data)
    fits_data = np.ndarray((1, data.size))
    fits_data[0] = data
    hdu = fits.PrimaryHDU(fits_data)
    hdu.writeto(filename, clobber=True)
    
    
# Main
if len(sys.argv) < 2:
  print("Usage: {} image.fit".format(sys.argv[0]), file=sys.stderr)
  sys.exit(1)

app = QApplication(sys.argv)

image_file = sys.argv[1]
print("Reading image file: " + image_file)
image_hdu = fits.open(image_file)
print(image_hdu.info())
for hdu in image_hdu:
  print(repr(hdu.header))

img_data = image_hdu[0].data
print("Type: {}, size: {}, ndim: {}, dtype: {}, shape: {}".format(type(img_data),img_data.size, img_data.ndim, img_data.dtype, img_data.shape) )

display_image = DisplayImage(img_data)
