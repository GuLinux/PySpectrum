from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

class FitsSpectrum:
    def __init__(self, fits_file):
        self.fits_file = fits_file
        self.reset()

    def calibrate(self, points, dispersion = -1):
        self.dispersion, self.x_start = np.polyfit([i['x'] for i in points], [i['wavelength'] for i in points], 1)
        
    def reset(self):
        header = self.fits_file[0].header
        self.dispersion = self.fits_file[0].header.get('CDELT1', 1)
        self.x_start = self.fits_file[0].header.get('CRVAL1', 0)
        
    def x_calibrated(self, value):
        return self.dispersion * value + self.x_start
    
    def x_uncalibrated(self, value):
        return (value-self.x_start)/self.dispersion
        
    def x_axis(self):
        return np.arange(0, self.data().size) * self.dispersion + self.x_start
    
    def data(self):
        return self.fits_file[0].data[0] if self.fits_file[0].header.get('NAXIS2', 0) == 1 else self.fits_file[0].data
    
    def plot_to(self, axes):
        axes.plot(self.x_axis(), self.data())
        axes.figure.canvas.draw()
            
    def save(self, filename):
        header = self.fits_file[0].header
        header['CRPIX1'] = 1
        header['CRVAL1'] = self.x_start
        header['CDELT1'] = self.dispersion
        
        