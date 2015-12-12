from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import traceback

class Spectrum:
    def __init__(self, fluxes, wavelengths = [], first_wavelength = 0, dispersion = 1):
        self.fluxes = fluxes
        print("lambdas: {}, first_wavelength: {}, dispersion: {}".format(wavelengths, first_wavelength, dispersion))
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
        indexes = [i for i, j in enumerate(self.wavelengths) if j <= wavelength]
        return indexes[-1] if indexes else 0
        
    def normalize_to_max(self):
        self.fluxes -= self.fluxes.min()
        self.fluxes /= self.fluxes.max()

class FitsSpectrum:
    CALIBRATION_DATA = 'CALIBRATION_DATA'
    SPECTRAL_LINES = 'SPECTRAL_LINES'
    LABELS = 'LABELS'
    
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
        if len(self.fits_file) > 1 and self.fits_file[1].name != FitsSpectrum.CALIBRATION_DATA and type(self.fits_file[1]) == fits.BinTableHDU:
            hdu = self.fits_file[1]
            columns = dict([('WAVELENGTH' if 'WAVE' in c.name.upper() else c.name.upper(), index) for index, c in enumerate(hdu.columns)])
            self.spectrum = Spectrum(fluxes=hdu.data.field(columns['FLUX']), wavelengths=hdu.data.field(columns['WAVELENGTH']))
            return
        
        header = self.fits_file[0].header
        dispersion = header.get('CDELT1', 1)
        x_start = header.get('CRVAL1', 0)
        fluxes = self.fits_file[0].data[0] if header.get('NAXIS2', 0) == 1 else self.fits_file[0].data
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
        
    def __add_table(self, name, columns):
        tbhdu = fits.BinTableHDU.from_columns(fits.ColDefs(columns))
        tbhdu.name = name
        for hdu in [h for h in self.fits_file if h.name == name]: self.fits_file.remove(hdu)
        self.fits_file.append(tbhdu)
            
    def save(self, filename, calibration_points = [], spectral_lines = [], labels = []):
        header = self.fits_file[0].header
        header.set('CRPIX1', comment='wavelength starting element', value=1)
        header.set('CRVAL1', comment='first wavelength, Angstrom', value=self.spectrum.wavelengths[0])
        header.set('CDELT1', comment='dispersion (Angstrom/pixel)', value = self.spectrum.dispersion())
        header.set('CD1_1', comment='dispersion (Angstrom/pixel)', value = self.spectrum.dispersion())
        header.set('CTYPE1', value = 'WAVE-WAV-PLY')
        header.set('CUNIT1', value = 'Angstrom')
        if len(spectral_lines) > 0:
            texts = fits.Column(name='text', format='20A', array=[line.name.encode() for line in spectral_lines])
            wavelengths = fits.Column(name='wavelength', format='D', array=[line.wavelength for line in spectral_lines])
            font_sizes = fits.Column(name='font_sizes', format='D', array=[line.fontsize for line in spectral_lines])
            show_lambdas = fits.Column(name='show_lambda', format='L', array=[line.show_lambda for line in spectral_lines])
            x_pos = fits.Column(name='x_pos', format='D', array=[line.position()[0] for line in spectral_lines])
            y_pos = fits.Column(name='y_pos', format='D', array=[line.position()[1] for line in spectral_lines])
            self.__add_table(FitsSpectrum.SPECTRAL_LINES, [texts, wavelengths, font_sizes, show_lambdas, x_pos, y_pos])
            
        if len(calibration_points) > 0:
            pixels = fits.Column(name='x_axis', format='K', array=[point['x'] for point in calibration_points])
            wavelengths = fits.Column(name='wavelength', format='D', array=[point['wavelength'] for point in calibration_points])
            self.__add_table(FitsSpectrum.CALIBRATION_DATA, [pixels, wavelengths])

        if len(labels) > 0:
            texts = fits.Column(name='text', format='500A', array=[line[1].get_text().encode() for line in labels])
            x = fits.Column(name='x', format='D', array=[line[1].position()[0] for line in labels])
            y = fits.Column(name='y', format='D', array=[line[1].position()[1] for line in labels])
            font_sizes = fits.Column(name='font_size', format='D', array=[line[1].get_size() for line in labels])
            types = fits.Column(name='type', format='15A', array=[line[0] for line in labels])
            self.__add_table(FitsSpectrum.LABELS, [texts, x, y, font_sizes, types])
            
        self.fits_file[0].data = self.spectrum.fluxes
        self.fits_file.writeto(filename, clobber=True)
        
    def __hdu_data(self, name):
        hdu = [h for h in self.fits_file if h.name == name]
        return hdu[-1].data if len(hdu) > 0 else []
    
    def __txt(fits_entry):
        return fits_entry.decode() if type(fits_entry) == bytes else fits_entry

    def labels(self):
        #text = label[0].decode() # Was this needed?
        return [{'text': FitsSpectrum.__txt(l[0]), 'coords': (l[1], l[2]), 'fontsize': l[3], 'type': l[4]} for l in self.__hdu_data(FitsSpectrum.LABELS)]
    
    def lines_labels(self):
        return [{'text': FitsSpectrum.__txt(s[0]), 'wavelength': s[1], 'fontsize': s[2], 'display_wavelength': s[3], 'position': (s[4], s[5])} for s in self.__hdu_data(FitsSpectrum.SPECTRAL_LINES)]
            
    def name(self):
        return self.fits_file.filename()

    
