from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

class FitsSpectrum:
    def __init__(self, fits_file):
        self.fits_file = fits_file
        self.reset()

    def calibrate(self, points):
        if len(points) == 0:
            self.reset()
            return
        
        if len(points) == 1:
            self.x_start = points[0]['wavelength'] -(self.dispersion*points[0]['x'])
            return
            
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
            
    def save(self, filename, calibration_points = []):
        header = self.fits_file[0].header
        header['CRPIX1'] = 1
        header['CRVAL1'] = self.x_start
        header['CDELT1'] = self.dispersion
        if len(calibration_points) > 0:
            pixels = fits.Column(name='x_axis', format='K', array=[point['x'] for point in calibration_points])
            wavelengths = fits.Column(name='wavelength', format='D', array=[point['wavelength'] for point in calibration_points])
            cols = fits.ColDefs([pixels, wavelengths])
            tbhdu = fits.BinTableHDU.from_columns(cols)
            tbhdu.name = 'CALIBRATION_DATA'
            #self.fits_file.remove('calibration_data') #TODO: remove, or keep for history?
            self.fits_file.append(tbhdu)
        print(filename)
        self.fits_file.writeto(filename, clobber=True)
        
    def name(self):
        return self.fits_file.filename()