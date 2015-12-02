from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QDateTime
from astropy.coordinates import SkyCoord
from astropy import units as u

class ViewObjectProperties(QWidget):
    def __init__(self, fits_file, parent = None):
        QWidget.__init__(self, parent)
        header = fits_file[0].header
        name=header['OBJECT']
        date=QDateTime.fromString(header['DATE'], Qt.ISODate)
        #header['CTYPE2'] TODO: get ra/dec from type
        ra=header['CRVAL2']
        #header['CTYPE3']
        dec=header['CRVAL3']
        type=header['OBJTYPE']
        sptype=header['SPTYPE']
        observer=header['OBSERVER']
        equipment = header['INSTRUMENT']
        position=header['POSITION']
        coords = SkyCoord(ra, dec, unit=u.deg)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(QLabel("Name: {}".format(name)))
        layout.addWidget(QLabel("Shoot date: {}".format(date.toString())))
        layout.addWidget(QLabel("Coordinates: {}".format(coords.to_string('hmsdms'))))
        layout.addWidget(QLabel("Type: {}, spectral class: {}".format(type, sptype)))
        layout.addWidget(QLabel("Observer: {}".format(observer)))
        layout.addWidget(QLabel("Equipment: {}".format(equipment)))
        layout.addWidget(QLabel("Position: {}".format(position)))
        
    def dialog(fits_file):
        dialog = QDialog()
        dialog.setWindowTitle("Object Properties")
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(ViewObjectProperties(fits_file, dialog))
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.clicked.connect(dialog.accept)
        dialog.layout().addWidget(button_box)
        return dialog