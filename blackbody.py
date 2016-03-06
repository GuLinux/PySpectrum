from fits_spectrum import *
from PyQt5.QtWidgets import QAction, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject
from collections import deque
import numpy as np
from astropy import units as u
from astropy.analytic_functions import blackbody_lambda, blackbody_nu
from astropy import constants as const
from fits_spectrum import *

class BlackBody:
    def __init__(self, kelvin):
        self.kelvin = kelvin * u.K
        
    def fluxes(self, start=0, wavemax=-1):
        if(wavemax < 0):
            wavemax = (const.b_wien / self.kelvin).to(u.AA)  # Wien's displacement law
        else:
            wavemax = wavemax * u.AA

        waveset = np.logspace(start, np.log10(wavemax.value + 10 * wavemax.value), num=1000) * u.AA
        with np.errstate(all='ignore'):
            flux = blackbody_lambda(waveset, self.kelvin)
        return waveset, flux
        
    def spectrum(self, start=0, wavemax=-1):
        wavelengths, fluxes= self.fluxes(start, wavemax)
        wavelengths = np.array([n.value for n in wavelengths])
        fluxes = np.array([n.value for n in fluxes])
        return Spectrum(fluxes, wavelengths)

class BlackBodyAction(QObject):
    def __init__(self, on_triggered, container):
        QObject.__init__(self)
        self.on_triggered = on_triggered
        self.blackbody_action = QAction("Blackbody radiation", self)
        self.blackbody_action.triggered.connect(self.blackbody_dialog)
        container.addAction(self.blackbody_action)
        
    def blackbody_dialog(self):
        ok = False
        kelvin = QInputDialog.getDouble(None, "Black Body Radiation", "Enter temperature for black body radiation (°K)", 0, 0)
        if(not kelvin[1]):
            return
        self.on_triggered( BlackBody(kelvin[0]) )
        
