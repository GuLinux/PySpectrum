from astroquery.simbad import Simbad
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox
from pyui.object_properties_dialog import Ui_ObjectPropertiesDialog
import re
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from astropy.coordinates import SkyCoord
from astropy import units as u

Simbad.add_votable_fields('otype(V)')
Simbad.add_votable_fields('sptype')

class ObjectPropertiesDialog(QDialog):
    properties_changed = pyqtSignal(dict)

    def __init__(self):
        super(ObjectPropertiesDialog, self).__init__()
        self.ui = Ui_ObjectPropertiesDialog()
        self.ui.setupUi(self)
        enable_simbad_button = lambda: self.ui.simbad.setEnabled(len(self.ui.name.currentText()))
        self.ui.name.editTextChanged.connect(lambda txt: enable_simbad_button())
        self.ui.name.lineEdit().returnPressed.connect(self.simbad_query)
        self.ui.simbad.clicked.connect(self.simbad_query)
        self.accepted.connect(self.emit_properties)
        enable_simbad_button()
        
    def simbad_query(self):
        result = Simbad.query_object(self.ui.name.currentText())
        if not result:
            QMessageBox.warning(self, 'Not Found', 'Identifier {} not recognized by Simbad'.format(self.ui.name.currentText()))
            return
        row = result[0] # todo: handle more than one results
        main_id = row['MAIN_ID'].decode()
        names = [(name[0].decode(), re.sub('\s{2,}', ' ', re.sub('^\*+', '', name[0].decode())).replace('NAME ', '').strip()) for name in Simbad.query_objectids(main_id)]
        names = [(n[0],n[1].title()) if n[0][0:4]=='NAME' else n for n in names]
        self.ui.name.clear()
        self.ui.name.addItems([name[1] for name in names])
        self.ui.name.setCurrentText([name[1] for name in names if main_id == name[0]][0])
        self.ui.ra.setText(row['RA'])
        self.ui.dec.setText(row['DEC'])
        self.ui.sptype.setText(row['SP_TYPE'].decode())
        self.ui.type.setText(row['OTYPE_V'].decode())
        
    def emit_properties(self):
        coords = SkyCoord(ra=self.ui.ra.text(), dec=self.ui.dec.text(), unit=(u.hourangle, u.deg))
        self.properties_changed.emit({
            'name': self.ui.name.currentText(),
            'ra': coords.ra.degree,
            'dec': coords.dec.degree,
            'type': self.ui.type.text(),
            'sptype': self.ui.sptype.text(),
            'date': self.ui.date.dateTime(),
            'observer': self.ui.author.text(),
            'instruments': self.ui.instruments.text(),
            'position': self.ui.location.text(),
            })
        
    def keyPressEvent(self, evt):
      if evt.key() == Qt.Key_Enter or evt.key() == Qt.Key_Return:
        return
        QDialog.keyPressEvent(self.evt)