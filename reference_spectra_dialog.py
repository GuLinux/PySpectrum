from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QSortFilterProxyModel

from reference_catalogues import ReferenceCatalogues
from ui_reference_spectra_dialog import Ui_ReferenceSpectraDialog

class ReferenceSpectraDialog(QDialog):
    
    fits_picked = pyqtSignal(str)
    
    def __init__(self, database):
        super(ReferenceSpectraDialog, self).__init__()
        self.ui = Ui_ReferenceSpectraDialog()
        self.ui.setupUi(self)
        self.reference_catalogues = ReferenceCatalogues(database)
        self.full_model = QStandardItemModel()
        self.catalogues_model = QStandardItemModel()
        self.ui.catalogue.setModel(self.catalogues_model)
        self.ui.catalogue.currentTextChanged.connect(lambda txt: self.populate())
        for catname, cat in self.reference_catalogues.catalogues.items():
            row = QStandardItem(catname)
            row.setData(cat)
            self.catalogues_model.appendRow(row)
        
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.full_model)
        self.model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.model.setFilterKeyColumn(0)
        self.ui.entries.setModel(self.model)
        self.ui.type_filter.currentTextChanged.connect(lambda txt: self.model.setFilterWildcard("{}*".format(txt) ) )
        self.ui.buttonBox.button(QDialogButtonBox.Open).setEnabled(False)
        self.ui.entries.selectionModel().selectionChanged.connect(lambda selected, deselected: self.ui.buttonBox.button(QDialogButtonBox.Open).setEnabled(len(selected.indexes()) > 0)  )
        self.accepted.connect(self.load_fits)
        self.populate()
            
    def populate(self):
        self.full_model.clear()
        catalogue = self.catalogues_model.item(self.ui.catalogue.currentIndex()).data()
        self.full_model.setHorizontalHeaderLabels(['Spectral Type'])
        entries = self.reference_catalogues.spectra(catalogue['name'])
        self.ui.type_filter.addItems( sorted(set([i['sptype'] for i in entries])) )
        
        for entry in entries:
            item = QStandardItem(entry['sptype'])
            item.setData(entry)
            self.full_model.appendRow(item)
        
            
    def load_fits(self):
        original_index = self.model.mapToSource(self.ui.entries.selectionModel().selectedIndexes()[0])
        entry = self.full_model.item(original_index.row()).data()
        self.fits_picked.emit(self.reference_catalogues.fits(entry))