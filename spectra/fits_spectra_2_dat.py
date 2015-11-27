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

class DisplayImage:
  def __init__(self, image):
    self.original = image.astype(float)
    self.rotated = self.original
    self.image_view = plt.imshow(self.original, cmap='gray')
    self.brotate = Button(self.image_view.figure.add_axes([0, 0.95, 0.1, 0.05]), "Rotate")
    self.bselect_background = Button(self.image_view.figure.add_axes([0.1, 0.95, 0.25, 0.05]), "Select Background")
    self.brotate.on_clicked(self.rotate)
    self.bselect_background.on_clicked(self.rotate)
    
    plt.figure()
    self.image_plot = plt.axes()
    self.degrees = (0, True)
    self.draw_plot()
    plt.show()
    
  def draw_plot(self):
    sums = self.rotated.sum(0)
    self.image_plot.clear()
    self.image_plot.plot(sums)
    self.image_plot.figure.canvas.draw()
    
  def rotate(self, evt):
    self.degrees = QInputDialog.getDouble(None, "Rotate", "Enter degrees for image rotation", self.degrees[0], 0, 360, 2)
    if not self.degrees[1]:
      return
    self.rotated = scipy.ndimage.interpolation.rotate(self.original, self.degrees[0])
    self.image_view.set_data(self.rotated)
    self.image_view.figure.canvas.draw()
    self.draw_plot()
    
    
if len(sys.argv) < 2:
  print >> sys.stderr, "Usage: " + sys.argv[0] + " image.fit"
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