from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QDateTime
from astropy.coordinates import SkyCoord
from astropy import units as u

class ObjectProperties:
    def __init__(self, fits_file):
        self.fits_file = fits_file
        self.read()

    def write(self):
        header = self.fits_file[0].header
        header.set('OBJECT', comment='Object display name', value=self.name)
        header.set('DATE', comment='Data acquisition date', value = self.date.toString(Qt.ISODate))
        header.set('CTYPE2', value = 'RA--TAN')
        header.set('CRVAL2', comment='Object right ascension in degrees', value= self.coordinates.ra.degree)
        header.set('CTYPE3', value = 'DEC--TAN')
        header.set('CRVAL3', comment='Object declination in degrees', value = self.coordinates.dec.degree)
        header.set('OBJTYPE', comment='Object type', value = self.type)
        header.set('SPTYPE', comment='Object spectral type', value = self.sptype)
        header.set('OBSERVER', value = self.observer)
        header.set('EQUIPMENT', value = self.equipment)
        header.set('POSITION', comment='Acquisition location', value = self.position)
        
    def read(self):
        header = self.fits_file[0].header
        self.name=header.get('OBJECT')
        self.date=QDateTime.fromString(header.get('DATE', QDateTime.currentDateTime().toString(Qt.ISODate)), Qt.ISODate)
        #header.get('CTYPE2') TODO: get ra/dec from type
        ra=header.get('CRVAL2', 0)
        #header.get('CTYPE3')
        dec=header.get('CRVAL3', 0)
        self.type=header.get('OBJTYPE')
        self.sptype=header.get('SPTYPE')
        self.observer=header.get('OBSERVER')
        self.equipment = header.get('INSTRUMENT')
        self.position=header.get('POSITION')
        self.coordinates = SkyCoord(ra, dec, unit=u.deg)
        
    def ra_str(self, unit=u.hourangle):
        return self.coordinates.ra.to_string(unit)
    
    def dec_str(self, unit=u.deg):
        return self.coordinates.dec.to_string(unit)
    
    def printable_coordinates(self):
        return self.coordinates.to_string('hmsdms')
    
class ViewObjectProperties(QWidget):
    def __init__(self, fits_file, parent = None):
        QWidget.__init__(self, parent)
        object_properties = ObjectProperties(fits_file)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(QLabel("Name: {}".format(object_properties.name)))
        layout.addWidget(QLabel("Shoot date: {}".format(object_properties.date.toString())))
        layout.addWidget(QLabel("Coordinates: {}".format(object_properties.printable_coordinates())))
        layout.addWidget(QLabel("Type: {}, spectral class: {}".format(object_properties.type, object_properties.sptype)))
        layout.addWidget(QLabel("Observer: {}".format(object_properties.observer)))
        layout.addWidget(QLabel("Equipment: {}".format(object_properties.equipment)))
        layout.addWidget(QLabel("Position: {}".format(object_properties.position)))
        
    def dialog(fits_file):
        dialog = QDialog()
        dialog.setWindowTitle("Object Properties")
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(ViewObjectProperties(fits_file, dialog))
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.clicked.connect(dialog.accept)
        dialog.layout().addWidget(button_box)
        return dialog