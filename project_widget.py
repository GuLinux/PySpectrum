from pyui.project_widget import Ui_ProjectWidget
from project import Project
from PyQt5.QtWidgets import QWidget, QToolBar
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from pyspectrum_commons import *
from import_image import ImportImage
from astropy.io import fits

class ProjectWidget(QWidget):
    import_image = pyqtSignal(str)
    calibrate = pyqtSignal(str)
    math = pyqtSignal(str)
    finish = pyqtSignal(str)
    
    def __init__(self, project, settings):
        QWidget.__init__(self)
        self.ui = Ui_ProjectWidget()
        self.ui.setupUi(self)
        self.project = project
        self.project.filesChanged.connect(self.refresh)
        self.toolbar = QToolBar()
        import_image = lambda: ImportImage.pick(lambda f: self.import_image.emit(f[0]), settings)
        self.toolbar.addAction(ImportImage.icon(), ImportImage.ACTION_TEXT, import_image)
        self.ui.import_image.clicked.connect(import_image)
        self.raw_spectra_model = QStandardItemModel()
        for model, widget, buttons in [
            (self.raw_spectra_model, self.ui.raw_spectra, [(self.ui.calibrate, self.calibrate)])
            ]:
            widget.setModel(model)
            for button in buttons:
                button[0].clicked.connect(lambda: button[1].emit(model.item(widget.selectionModel().selectedRows()[0].row()).data() ))
                widget.selectionModel().selectionChanged.connect(lambda sel, unsel: button[0].setEnabled(len(sel.indexes())>0))
            
        self.refresh()
        
    def refresh(self):
        self.ui.name.setText(self.project.get_name())
        self.ui.observer.setText(self.project.get_observer())
        self.ui.position.setText(self.project.get_position())
        self.ui.equipment.setText(self.project.get_equipment())
        self.ui.date.setText(self.project.get_date().toString())
        for model, items in [
            (self.raw_spectra_model, self.project.get_raw_profiles())
            ]:
            model.clear()
            model.setHorizontalHeaderLabels(['Object', 'Last Modified'])
            for item in items:
                file = item[1]
                name = fits.getheader(file)['OBJECT']
                file_item = QStandardItem(name)
                file_item.setData(file)
                model.appendRow([file_item, QStandardItem(item[0].toString())])
