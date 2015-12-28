from PyQt5.QtWidgets import QDialog, QAction, QDoubleSpinBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from pyui.spectrum_trim_dialog import Ui_SpectrumTrimDialog

class SpectrumTrimDialog(QDialog):
    def __init__(self, spectrum, direction, axes, redraw, parent = None, before_removal = None):
        QDialog.__init__(self, parent)
        self.spectrum = spectrum
        self.direction = direction
        self.axes = axes
        self.redraw = redraw
        self.before_removal = before_removal
        
        self.ui = Ui_SpectrumTrimDialog()
        self.ui.setupUi(self)
        self.ui.wavelength.setRange(spectrum.wavelengths[0], spectrum.wavelengths[-1])
        self.ui.wavelength.setValue(spectrum.wavelengths[0] if direction == 'before' else spectrum.wavelengths[-1])
        self.value_line = axes.axvline(self.ui.wavelength.value(), color='red')

        self.connection = axes.figure.canvas.mpl_connect('button_press_event', self.__double_click_axes )
        axes.figure.canvas.draw()
            
        self.ui.wavelength.valueChanged.connect(self.__move_line)
        self.ui.buttonBox.accepted.connect(self.__remove_data)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.finished.connect(self.__cleanup)
        
    def __double_click_axes(self, ev):
        if ev.dblclick:
            self.__move_line(ev.xdata)
            self.ui.wavelength.setValue(ev.xdata)
            
            
    def __cleanup(self):
        self.axes.figure.canvas.mpl_disconnect(self.connection)
        self.value_line.remove()
        self.deleteLater()
        
    def __remove_data(self):
        self.accept()
        if self.before_removal:
            self.before_removal()
        point = self.ui.wavelength.value()
        if self.direction == 'before':
            self.spectrum.cut(start=self.spectrum.wavelength_index(point))
        else:
            self.spectrum.cut(end=self.spectrum.wavelength_index(point))
            
        self.spectrum.normalize_to_max()
        self.redraw()
        
    @pyqtSlot(float)
    def __move_line(self, wavelength):
        canvas = self.axes.figure.canvas
        background = canvas.copy_from_bbox(self.axes.bbox)
        self.value_line.set_xdata(wavelength)
        self.axes.draw_artist(self.value_line)
        canvas.blit(self.axes.bbox)
        canvas.restore_region(background)