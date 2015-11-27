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
  def __init__(self, image):
    self.config = QSettings('GuLinux', 'PySpectra')
    self.original = image.astype(float)
    self.rotated = self.original
    self.background = np.zeros((1,1), float)
    self.image_view = plt.imshow(self.original, cmap='gray')
    self.brotate = Button(self.image_view.figure.add_axes([0, 0.95, 0.1, 0.05]), "Rotate")
    self.bselect_background = Button(self.image_view.figure.add_axes([0.1, 0.95, 0.25, 0.05]), "Select Background")
    self.bsave = Button(self.image_view.figure.add_axes([0.1 + 0.25, 0.95, 0.1, 0.05]), "Save")
    self.brotate.on_clicked(self.rotate)
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
    self.degrees = (0, True)
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
    
  def draw_plot(self):
    sums = (self.rotated - self.background.mean()).sum(0)
    self.image_plot.clear()
    self.image_plot.plot(sums)
    self.image_plot.figure.canvas.draw()
    
  def select_bg(self, evt):
    self.RS.set_active(True)
    
  def rotate(self, evt):
    self.degrees = QInputDialog.getDouble(None, "Rotate", "Enter degrees for image rotation", self.degrees[0], 0, 360, 2)
    if not self.degrees[1]:
      return
    self.rotated = scipy.ndimage.interpolation.rotate(self.original, self.degrees[0])
    self.image_view.set_data(self.rotated)
    self.image_view.figure.canvas.draw()
    self.draw_plot()
    
  def save(self, ev):
    save_file = QFileDialog.getSaveFileName(None, "Save plot...", self.config.value('last_save_dir'), "*FITS file (.fit *.fits)")
    if not save_file[0]:
      return
    filename = save_file[0]
    self.config.setValue('last_save_dir', os.path.dirname(os.path.realpath(filename)))
    print(filename)
    
    
if len(sys.argv) < 2:
  print("Usage: {} image.fit".format(sys.argv[0]), file=sys.stderr)
  sys.exit(1)

image_file = sys.argv[1]
print("Reading image file: " + image_file)
image_hdu = fits.open(image_file)
print(image_hdu.info())
for hdu in image_hdu:
  print(repr(hdu.header))

img_data = image_hdu[0].data
print("Type: {}, size: {}, ndim: {}, dtype: {}, shape: {}".format(type(img_data),img_data.size, img_data.ndim, img_data.dtype, img_data.shape) )

display_image = DisplayImage(img_data)
