from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import traceback

class Spectrum:
    def __init__(self, fluxes, wavelengths = [], first_wavelength = 0, dispersion = 1):
        self.fluxes = fluxes
        self.wavelengths = wavelengths if len(wavelengths) > 0 else self.__calculate_wavelengths(dispersion, first_wavelength)

    def dispersion(self):
        return (self.wavelengths[-1]-self.wavelengths[0])/(len(self.wavelengths)-1)
    
    def __calculate_wavelengths(self, m, q):
        return np.fromfunction(lambda x: m*x+q, self.fluxes.shape)
        
    def calibrate(self, points=[], dispersion=None):
        if len(points) == 1 and dispersion:
            q = points[0]['wavelength'] - dispersion*points[0]['x']
            self.wavelengths = self.__calculate_wavelengths(dispersion, q)
            
        if len(points) > 1 and dispersion == None:
            m, q = np.polyfit([i['x'] for i in points], [i['wavelength'] for i in points], 1)
            self.wavelengths = self.__calculate_wavelengths(m, q)
    
    def cut(self, start = 0, end = -1):
        end = len(self.wavelengths) if end == -1 else end+1
        self.wavelengths = self.wavelengths[start:end]
        self.fluxes = self.fluxes[start:end]
        
    def wavelength_index(self, wavelength):
        return [i for i, j in enumerate(self.wavelengths) if j <= wavelength][-1]
        
    def normalize_to_max(self):
        self.fluxes /= self.fluxes.max()

class FitsSpectrum:
    CALIBRATION_DATA = 'CALIBRATION_DATA'
    SPECTRAL_LINES = 'SPECTRAL_LINES'
    
    def __init__(self, fits_file):
        self.fits_file = fits_file
        self.reset()

    def calibrate(self, points, dispersion):
        if len(points) == 0:
            self.reset()
            return
        
        if len(points) == 1:
            self.spectrum.calibrate(points, dispersion)
            #self.x_start = points[0]['wavelength'] -(self.dispersion*points[0]['x'])
            return
        self.spectrum.calibrate(points)
        #self.dispersion, self.x_start = np.polyfit([i['x'] for i in points], [i['wavelength'] for i in points], 1)
        

    def reset(self):
        if len(self.fits_file) > 1 and self.fits_file[1].name != FitsSpectrum.CALIBRATION_DATA:
            hdu = self.fits_file[1]
            columns = dict([('WAVELENGTH' if 'WAVE' in c.name.upper() else c.name.upper(), index) for index, c in enumerate(hdu.columns)])
            self.spectrum = Spectrum(fluxes=hdu.data.field(columns['FLUX']), wavelengths=hdu.data.field(columns['WAVELENGTH']))
            return
        
        header = self.fits_file[0].header
        dispersion = self.fits_file[0].header.get('CDELT1', 1)
        x_start = self.fits_file[0].header.get('CRVAL1', 0)
        fluxes = self.fits_file[0].data[0] if self.fits_file[0].header.get('NAXIS2', 0) == 1 else self.fits_file[0].data
        self.spectrum = Spectrum(fluxes, first_wavelength = x_start, dispersion = dispersion)

    def data(self):
        print("DEPRECATED CALL to data")
        traceback.print_stack()
        return self.spectrum.fluxes
        #return self.fits_file[0].data[0] if self.fits_file[0].header.get('NAXIS2', 0) == 1 else self.fits_file[0].data

        
    def plot_to(self, axes):
        axes.plot(self.spectrum.wavelengths, self.spectrum.fluxes)
        axes.figure.tight_layout()
        axes.figure.canvas.draw()
            
    def save(self, filename, calibration_points = [], spectral_lines = []):
        header = self.fits_file[0].header
        header['CRPIX1'] = 1
        header['CRVAL1'] = self.spectrum.wavelengths[0]
        header['CDELT1'] = self.spectrum.dispersion()
        if len(spectral_lines) > 0:
            texts = fits.Column(name='text', format='20A', array=[line.name for line in spectral_lines])
            wavelengths = fits.Column(name='wavelength', format='D', array=[line.wavelength for line in spectral_lines])
            font_sizes = fits.Column(name='font_sizes', format='D', array=[line.fontsize for line in spectral_lines])
            show_lambdas = fits.Column(name='show_lambda', format='L', array=[line.show_lambda for line in spectral_lines])
            x_pos = fits.Column(name='x_pos', format='D', array=[line.position()[0] for line in spectral_lines])
            y_pos = fits.Column(name='y_pos', format='D', array=[line.position()[1] for line in spectral_lines])
            cols = fits.ColDefs([texts, wavelengths, font_sizes, show_lambdas, x_pos, y_pos])
            tbhdu = fits.BinTableHDU.from_columns(cols)
            tbhdu.name = FitsSpectrum.SPECTRAL_LINES
            for hdu in [h for h in self.fits_file if h.name == FitsSpectrum.SPECTRAL_LINES]: self.fits_file.remove(hdu)
            self.fits_file.append(tbhdu)
            
        if len(calibration_points) > 0:
            pixels = fits.Column(name='x_axis', format='K', array=[point['x'] for point in calibration_points])
            wavelengths = fits.Column(name='wavelength', format='D', array=[point['wavelength'] for point in calibration_points])
            cols = fits.ColDefs([pixels, wavelengths])
            tbhdu = fits.BinTableHDU.from_columns(cols)
            tbhdu.name = FitsSpectrum.CALIBRATION_DATA
            for hdu in [h for h in self.fits_file if h.name == FitsSpectrum.CALIBRATION_DATA]: self.fits_file.remove(hdu)
            self.fits_file.append(tbhdu)
        self.fits_file[0].data = self.spectrum.fluxes
        self.fits_file.writeto(filename, clobber=True)
        
    def name(self):
        return self.fits_file.filename()

    