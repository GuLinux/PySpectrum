import unittest
from fits_spectrum import Spectrum
import numpy as np
from numpy.testing import *

class TestSpectrum(unittest.TestCase):

    def test_calc_dispersion(self):
        spectrum = Spectrum(np.array([0.2, 0.3, 0.5]), np.array([0, 1, 2]))
        self.assertEqual(spectrum.dispersion(), 1)
      
        spectrum = Spectrum(np.array([0.2, 0.3, 0.5]), np.array([0, 2.5, 5]))
        self.assertEqual(spectrum.dispersion(), 2.5)
      
    def test_empty_wavelengths(self):
        spectrum = Spectrum(np.array([0.2, 0.3, 0.5]))
        assert_array_equal(spectrum.wavelengths, [0, 1, 2])
        
        spectrum = Spectrum(np.array([0.2, 0.3, 0.5]), first_wavelength=5, dispersion=2)
        assert_array_equal(spectrum.wavelengths, [5, 7,9])
      
    def test_calibrate(self):
        spectrum = Spectrum(np.array([0.2, 0.3, 0.5]), np.array([3, 4, 5]))
        spectrum.calibrate(points=[{'x':1, 'wavelength':2}], dispersion=4)
        assert_array_equal(spectrum.wavelengths, [-2., 2., 6.])
        
        spectrum = Spectrum(np.array([0.2, 0.3, 0.5, 0.7]), np.array([3, 4, 5]))
        spectrum.calibrate(points=[{'x':1, 'wavelength':3.}, {'x': 2, 'wavelength': 9.}])
        assert_array_almost_equal(spectrum.wavelengths, [-3., 3., 9., 15.])
        
    def test_cut(self):
        spectrum = Spectrum(np.array([0.2, 0.3, 0.5, 0.7]), np.array([3, 6, 9, 12]))
        spectrum.cut(start=1)
        assert_array_equal(spectrum.wavelengths, [6, 9, 12])
        assert_array_equal(spectrum.fluxes, [0.3, 0.5, 0.7])
        
        spectrum = Spectrum(np.array([0.2, 0.3, 0.5, 0.7]), np.array([3, 6, 9, 12]))
        spectrum.cut(end=2)
        assert_array_equal(spectrum.wavelengths, [3, 6, 9])
        assert_array_equal(spectrum.fluxes, [0.2, 0.3, 0.5])
        
        spectrum = Spectrum(np.array([0.2, 0.3, 0.5, 0.7]), np.array([3, 6, 9, 12]))
        spectrum.cut(start=1,end=2)
        assert_array_equal(spectrum.wavelengths, [6, 9])
        assert_array_equal(spectrum.fluxes, [0.3, 0.5])
        
        
        

if __name__ == '__main__':
    unittest.main()