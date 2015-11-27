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
from calibrate_dialog import *

class Calibrate:
    def __init__(self, fits_file):
        self.config = QSettings('GuLinux', 'PySpectra')
        self.fits_file = fits_file
        self.__init_plot__()
        self.bcalibrate = Button(self.image_plot.figure.add_axes([0, 0.95, 0.1, 0.05]), "Calibrate")
        self.bsave = Button(self.image_plot.figure.add_axes([0.1 , 0.95, 0.1, 0.05]), "Save")
        self.bcalibrate.on_clicked(lambda ev: self.calibrate() )
        self.bsave.on_clicked(lambda ev: self.save() )
        self.calibrate_dialog = QDialog()
        self.calibrate_dialog_ui = Ui_Calibrate()
        self.calibrate_dialog_ui.setupUi(self.calibrate_dialog)

        self.calibrate_dialog_ui.first_point_lambda.setRange(0, 50000)
        self.calibrate_dialog_ui.second_point_lambda.setRange(0, 50000)
        self.calibrate_dialog_ui.first_point_pixel.setRange(0, self.data()[0].size)
        self.calibrate_dialog_ui.second_point_pixel.setRange(0, self.data()[0].size)

        self.calibrate_dialog.accepted.connect(self.calibrated)
        plt.show()

    def calibrate(self):
        self.calibrating = True
        self.calibrate_dialog.show()

    def calibrated(self):
        self.calibrating = False
        dispersion = (self.calibrate_dialog_ui.second_point_lambda.value() - self.calibrate_dialog_ui.first_point_lambda.value()) / (self.calibrate_dialog_ui.second_point_pixel.value() - self.calibrate_dialog_ui.first_point_pixel.value())
        starting_wavelength = self.calibrate_dialog_ui.first_point_lambda.value() - (self.calibrate_dialog_ui.first_point_pixel.value() * dispersion)
        header = self.fits_file[0].header
        header['CRPIX1'] = 1
        header['CRVAL1'] = starting_wavelength
        header['CDELT1'] = dispersion
        print("calibrate: starting_wavelength={}, dispersion={}".format(starting_wavelength, dispersion))

    def data(self):
        return self.fits_file[0].data

    def __init_plot__(self):
        plt.figure()
        self.image_plot = plt.axes()
        self.draw_plot()
        

    def draw_plot(self):
        self.image_plot.clear()
        self.image_plot.plot(self.data()[0])
        self.image_plot.figure.canvas.draw()

    def save(self):
        save_file = QFileDialog.getSaveFileName(None, "Save plot...", self.config.value('last_save_dir'), "FITS file (.fit)")
        if not save_file[0]:
            return
        filename = save_file[0]
        self.fits_file.writeto(filename, clobber=True)

# TODO: plotting calibrated spectrum; colormap as following:
#       plt.cm.nipy_spectral(1.0)

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

calibrate = Calibrate(image_hdu)
