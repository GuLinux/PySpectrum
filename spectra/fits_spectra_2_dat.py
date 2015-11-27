#!/bin/python
import astropy
from astropy.io import fits
import sys
import numpy as np

import matplotlib.pyplot as plt
import time
import scipy.ndimage.interpolation
from matplotlib.widgets import Button



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

degrees = 0
#rotated = scipy.ndimage.interpolation.rotate(img_data, 20)
#toolbar = plt.NavigationToolbar()

plot = plt.imshow(img_data, cmap='gray')
brot_ax = plt.axes([0, 0.95, 0.1, 0.05])
brotate = Button(brot_ax, "Rotate")
brotate.on_clicked(lambda pos:print("foo %d" % pos.button))
plt.show()
