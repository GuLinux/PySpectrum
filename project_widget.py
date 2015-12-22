from pyui.project_widget import Ui_ProjectWidget
from project import Project
from PyQt5.QtWidgets import QWidget, QToolBar, QMenu, QHeaderView
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QUrl
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QDesktopServices
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
        self.calibrated_spectra_model = QStandardItemModel()
        self.finished_spectra_model = QStandardItemModel()

        def button_action(button, signal, widget, model):
            button.clicked.connect(lambda: signal.emit(model.item(widget.selectionModel().selectedRows()[0].row()).data() ) )
            widget.selectionModel().selectionChanged.connect(lambda sel, unsel: button.setEnabled(len(sel.indexes())>0))
            
        for model, widget in [(self.raw_spectra_model, self.ui.raw_spectra), (self.calibrated_spectra_model, self.ui.calibrated_spectra), (self.finished_spectra_model, self.ui.finished_spectra)]:
            widget.setModel(model)
            widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            
        button_action(self.ui.calibrate, self.calibrate, self.ui.raw_spectra, self.raw_spectra_model)
        button_action(self.ui.math, self.math, self.ui.calibrated_spectra, self.calibrated_spectra_model)
        button_action(self.ui.finish, self.finish, self.ui.calibrated_spectra, self.calibrated_spectra_model)
        button_action(self.ui.open_finished, self.finish, self.ui.finished_spectra, self.finished_spectra_model)
        open_finished_menu = QMenu()
        self.ui.open_finished_dirs.setMenu(open_finished_menu)
        open_finished_menu.addAction(QIcon(':/image_20'), 'Exported Images folder', lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(project.directory_path(Project.EXPORTED_IMAGES))))
        open_finished_menu.addAction(QIcon(':/done_20'), 'Finished Spectra folder', lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(project.directory_path(Project.FINISHED_PROFILES))))
        

            
        self.refresh()
        
    def refresh(self):
        self.ui.name.setText(self.project.get_name())
        self.ui.observer.setText(self.project.get_observer())
        self.ui.position.setText(self.project.get_position())
        self.ui.equipment.setText(self.project.get_equipment())
        self.ui.date.setText(self.project.get_date().toString())
        for model, items in [
            (self.raw_spectra_model, self.project.get_raw_profiles()),
            (self.calibrated_spectra_model, self.project.get_calibrated_profiles()),
            (self.finished_spectra_model, self.project.get_finished_profiles())
            ]:
            model.clear()
            model.setHorizontalHeaderLabels(['Object', 'Last Modified', 'Comment'])
            for item in items:
                file = item[1]
                header = fits.getheader(file)
                name = header.get('OBJECT', os.path.basename(file))
                comment = header.get('NOTES', '')
                file_item = QStandardItem(name)
                file_item.setData(file)
                model.appendRow([file_item, QStandardItem(item[0].toString()), QStandardItem(comment)])
