from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

class FitsSpectrum:
    def __init__(self, fits_file):
        self.fits_file = fits_file

    def calibrate(self, m, q):
        header = self.fits_file[0].header
        header['CRPIX1'] = 1
        header['CRVAL1'] = q
        header['CDELT1'] = m
        
    def x_axis(self):
        header = self.fits_file[0].header
        q = header.get('CRVAL1', 0)
        m = header.get('CDELT1', 1)
        return np.arange(0, self.data().size) * m + q
    
    def data(self):
        return self.fits_file[0].data[0] if self.fits_file[0].header.get('NAXIS2', 0) == 1 else self.fits_file[0].data
    
    def plot_to(self, axes):
        axes.plot(self.x_axis(), self.data())
        axes.figure.canvas.draw()