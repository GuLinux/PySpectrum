from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QDateTime
from astropy.coordinates import SkyCoord
from astropy import units as u

class ObjectProperties:
    def __init__(self, fits_file):
        header = fits_file[0].header
        self.name=header['OBJECT']
        self.date=QDateTime.fromString(header['DATE'], Qt.ISODate)
        #header['CTYPE2'] TODO: get ra/dec from type
        ra=header['CRVAL2']
        #header['CTYPE3']
        dec=header['CRVAL3']
        self.type=header['OBJTYPE']
        self.sptype=header['SPTYPE']
        self.observer=header['OBSERVER']
        self.equipment = header['INSTRUMENT']
        self.position=header['POSITION']
        self.coordinates = SkyCoord(ra, dec, unit=u.deg)
        
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