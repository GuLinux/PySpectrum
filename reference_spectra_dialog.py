from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QSortFilterProxyModel

from reference_catalogues import ReferenceCatalogues
from pyui.reference_spectra_dialog import Ui_ReferenceSpectraDialog
from qtcommons import *
from pyspectrum_commons import *
from fits_spectrum import FitsSpectrum
from astropy.io import fits
from matplotlib.lines import Line2D

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
        self.ui.type_filter.clear()
        self.ui.type_filter.addItem('')
        self.ui.type_filter.addItems( sorted(set([i['sptype'] for i in entries])) )
        
        for entry in entries:
            item = QStandardItem(entry['sptype'])
            item.setData(entry)
            self.full_model.appendRow(item)
            
    def load_fits(self):
        original_index = self.model.mapToSource(self.ui.entries.selectionModel().selectedIndexes()[0])
        entry = self.full_model.item(original_index.row()).data()
        self.fits_picked.emit(self.reference_catalogues.fits(entry))
        
        
    def setup_menu(self, toolbar, axes):
        self.current_line = None
        reference_action = QtCommons.addToolbarPopup(toolbar, "Reference")
        reference_action.menu().addAction("Reference library", lambda: self.show())
        reference_action.menu().addAction("Load from FITS file", lambda: QtCommons.open_file('Open Reference Profile', FITS_EXTS, lambda f: self.__open_reference(f[0], axes)))
        self.close_action = reference_action.menu().addAction("Close", lambda: self.__close_reference(axes))
        self.close_action.setEnabled(False)
        self.fits_picked.connect(lambda f: self.__open_reference(f, axes))

    def __open_reference(self, file, axes):
        fits_spectrum = FitsSpectrum(fits.open(file))
        fits_spectrum.spectrum.normalize_to_max()
        self.current_line = Line2D(fits_spectrum.spectrum.wavelengths, fits_spectrum.spectrum.fluxes, color='gray')
        axes.add_line(self.current_line)
        axes.figure.canvas.draw()
        self.close_action.setEnabled(True)
        
    def __close_reference(self, axes):
        self.close_action.setEnabled(False)
        if self.current_line:
            self.current_line.remove()
            self.current_line = None
            axes.figure.canvas.draw()
