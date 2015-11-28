from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QSortFilterProxyModel

from miles import Miles
from ui_miles_dialog import Ui_MilesDialog

class MilesDialog(QDialog):
    
    fits_picked = pyqtSignal(str)
    
    def __init__(self):
        super(MilesDialog, self).__init__()
        self.ui = Ui_MilesDialog()
        self.ui.setupUi(self)
        self.miles = Miles()
        self.full_model = QStandardItemModel()
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.full_model)
        self.model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.model.setFilterKeyColumn(1)
        self.ui.miles_entries.setModel(self.model)
        self.full_model.setHorizontalHeaderLabels(['Star', 'Spectral Type'])
        self.ui.type_filter.addItems( sorted(set([i['spectral-type'] for i in self.miles.catalog])) )
        self.ui.type_filter.currentTextChanged.connect(lambda txt: self.model.setFilterWildcard("{}*".format(txt) ) )
        self.ui.buttonBox.button(QDialogButtonBox.Open).setEnabled(False)
        self.ui.miles_entries.selectionModel().selectionChanged.connect(lambda selected, deselected: self.ui.buttonBox.button(QDialogButtonBox.Open).setEnabled(len(selected.indexes()) > 0)  )
        self.accepted.connect(self.load_fits)
        for entry in self.miles.catalog:
            star_name = QStandardItem(entry['star-name'])
            star_name.setData(entry['miles-number'])
            self.full_model.appendRow([star_name, QStandardItem(entry['spectral-type'])])
            
    def load_fits(self):
        original_index = self.model.mapToSource(self.ui.miles_entries.selectionModel().selectedIndexes()[0])
        number = self.full_model.item(original_index.row()).data()
        self.fits_picked.emit(self.miles.fits(number))