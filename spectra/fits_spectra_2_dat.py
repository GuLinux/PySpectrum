#!/bin/python
import astropy
from astropy.io import fits
import sys
import numpy as np
import cv2
from cv2 import *


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
print type(img_data)

cv2.imshow('image', img_data)
cv2.waitKey(0)
