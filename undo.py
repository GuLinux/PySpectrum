from fits_spectrum import *
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject
from collections import deque

class Undo(QObject):
    def __init__(self, spectrum, redraw):
        QObject.__init__(self)
        self.redraw = redraw
        self.undo_action = QAction(QIcon(":/undo_20.png"), "Undo", self)
        self.redo_action = QAction(QIcon(":/redo_20.png"), "Redo", self)
        self.undo_action.triggered.connect(self.undo)
        self.redo_action.triggered.connect(self.redo)
        self.set_spectrum(spectrum)
        
    def undo(self):
        data = self.undo_buffer.pop()
        self.__append_to_buffer(self.__current_data(), self.redo_buffer)
        self.__reset_data(data)
        
    def redo(self):
        data = self.redo_buffer.pop()
        self.__append_to_buffer(self.__current_data(), self.undo_buffer)
        self.__reset_data(data)
        
    def save_undo(self):
        self.__append_to_buffer( self.__current_data(), self.undo_buffer)
        self.redo_buffer.clear()
        self.__enable_actions()
        
    def __reset_data(self, data):
        self.spectrum.wavelengths = data[0]
        self.spectrum.fluxes = data[1]
        self.__enable_actions()
        self.redraw()
        
    def set_spectrum(self, spectrum):
        self.spectrum = spectrum
        self.undo_buffer = deque(maxlen=20)
        self.redo_buffer = deque(maxlen=20)
        self.__enable_actions()
        
    def __enable_actions(self):
        self.undo_action.setEnabled(len(self.undo_buffer)>0)
        self.redo_action.setEnabled(len(self.redo_buffer)>0)
        
    def __append_to_buffer(self, data, buffer):
        buffer.append((np.copy(data[0]), np.copy(data[1])))
        
    def __current_data(self):
        return self.spectrum.wavelengths, self.spectrum.fluxes