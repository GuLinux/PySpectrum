from pyui.homepage import Ui_HomePage
from PyQt5.QtWidgets import QApplication
from pyspectrum_commons import *
from PyQt5.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QCheckBox, QLabel, QDialogButtonBox, QProgressDialog, QMessageBox
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from qtcommons import QtCommons
from PyQt5.QtWidgets import QWidget, QToolBar
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from reference_catalogues import ReferenceCatalogues
from project import Project
from import_image import ImportImage

class HomePage(QWidget):
    stack_images = pyqtSignal(str)
    import_image = pyqtSignal(str)
    calibrate = pyqtSignal(str)
    math = pyqtSignal(str)
    finish = pyqtSignal(str)
    new_project = pyqtSignal()
    open_project = pyqtSignal(str)

    def __init__(self, settings, database):
        QWidget.__init__(self)
        last_files_list = LastFilesList(settings)
        self.settings = settings
        self.database = database
        self.ui = Ui_HomePage()
        self.ui.setupUi(self)
        self.toolbar = QToolBar()
        welcome_text = "{} {}".format(QApplication.instance().applicationName(), QApplication.instance().applicationVersion())
        self.ui.welcome_label.setText(self.ui.welcome_label.text().format(welcome_text))
        file_action = QtCommons.addToolbarPopup(self.toolbar, 'File', icon_file=':/file_20')
        project_action = QtCommons.addToolbarPopup(self.toolbar, 'Project', icon_file=':/project_20')
        #file_action.menu().addAction(QIcon(':/stack_20'), 'Stack Images', lambda: open_file_sticky('Open Reference FITS Image',FITS_IMG_EXTS, lambda f: self.stack_images.emit(f[0]), settings, IMPORT_IMG ))
        import_image_action = lambda: ImportImage.pick(lambda f: self.import_image.emit(f[0]), settings)
        file_action.menu().addAction(ImportImage.icon(), ImportImage.ACTION_TEXT, import_image_action)
        self.ui.import_image.clicked.connect(import_image_action)
        file_action.menu().addAction(QIcon(':/plot_20'), 'Calibrate Spectrum', lambda: open_file_sticky('Open raw FITS Spectrum',FITS_EXTS, lambda f: self.calibrate.emit(f[0]), settings, RAW_PROFILE, [IMPORT_IMG] ))
        file_action.menu().addAction(QIcon(':/math_20'), 'Spectra Math', lambda: self.math.emit(None) )
        file_action.menu().addAction(QIcon(':/done_20'), 'Finish Spectrum', lambda: open_file_sticky('Open FITS Spectrum',FITS_EXTS, lambda f: self.finish.emit(f[0]), settings, CALIBRATED_PROFILE, [RAW_PROFILE,IMPORT_IMG] ))
        
        project_action.menu().addAction(QIcon(':/project_new_20'), 'New', lambda: self.new_project.emit())
        
        pick_project = lambda: open_directory_sticky('Open Project', self.__project_picked, settings, PROJECTS)
        self.ui.pick_project.clicked.connect(pick_project)
        project_action.menu().addAction(QIcon(':/new_open_20'), 'Open...', pick_project)
        
        self.recent_raw_model = QStandardItemModel()
        self.recent_calibrated_model = QStandardItemModel()
        self.recent_projects_model = QStandardItemModel()
        self.ui.recent_raw_list.setModel(self.recent_raw_model)
        self.ui.recent_calibrated_list.setModel(self.recent_calibrated_model)
        self.ui.recent_projects.setModel(self.recent_projects_model)
        LastFilesList.instance().files_changed.connect(self.__populate_lists)
        selected_path = lambda model, view: model.item(view.selectionModel().selectedRows()[0].row()).data()
        button_enable = lambda view, button: view.selectionModel().selectionChanged.connect(lambda sel, desel: button.setEnabled(len(sel.indexes() )) )
        
        button_enable(self.ui.recent_raw_list, self.ui.calibrate)
        button_enable(self.ui.recent_calibrated_list, self.ui.math)
        button_enable(self.ui.recent_calibrated_list, self.ui.finish)
        button_enable(self.ui.recent_projects, self.ui.open_recent_project)
        self.ui.calibrate.clicked.connect(lambda: self.calibrate.emit(selected_path(self.recent_raw_model, self.ui.recent_raw_list)))
        self.ui.math.clicked.connect(lambda: self.math.emit(selected_path(self.recent_calibrated_model, self.ui.recent_calibrated_list)))
        self.ui.finish.clicked.connect(lambda: self.finish.emit(selected_path(self.recent_calibrated_model, self.ui.recent_calibrated_list)))
        self.ui.open_recent_project.clicked.connect(lambda: self.open_project.emit(selected_path(self.recent_projects_model, self.ui.recent_projects)))
        self.ui.new_project.clicked.connect(self.new_project.emit)
        self.reference_catalogues = ReferenceCatalogues(database)
        
        self.ui.download_catalogs.clicked.connect(self.download_catalogs)
        self.__populate_lists()

    def __project_picked(self, file):
        try:
            project = Project(file[0])
            self.open_project.emit(project.path)
        except FileNotFoundError:
            QMessageBox.warning(self, 'Project not found', 'Missing or invalid project specified')

    def __populate_lists(self):
        get_names = {
            RAW_PROFILE: ('File', lambda n, p: n),
            CALIBRATED_PROFILE: ('File', lambda n, p: n ),
            PROJECTS: ('Name', lambda n, p: Project(p).get_name() )
            }
        for key, model in [(RAW_PROFILE, self.recent_raw_model), (CALIBRATED_PROFILE, self.recent_calibrated_model), (PROJECTS, self.recent_projects_model)]:
            model.clear()
            for name, dir, path in LastFilesList.instance().last_files(key):
                try:
                    model.setHorizontalHeaderLabels([get_names[key][0], "Directory"])
                    print("{}: {}-{}-{}".format(key, name, dir, path))
                    item = QStandardItem(get_names[key][1](name, path))
                    item.setData(path)
                    model.appendRow([item, QStandardItem(dir)])
                except:
                    pass
    
    def download_catalogs(self):
        dialog = QDialog()
        dialog.setWindowTitle('Download Catalogs')
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(QLabel('Select catalogues to be downloaded'))
        checkboxes = dict([(c, QCheckBox(c)) for c in self.reference_catalogues.catalogues])
        for name, checkbox in checkboxes.items():
            checkbox.setChecked(True)
            dialog.layout().addWidget(checkbox)
        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(dialog.accept)
        buttonbox.rejected.connect(dialog.reject)
        dialog.layout().addWidget(buttonbox)
        if dialog.exec() == QDialog.Rejected:
            return
        for cat, checkbox in checkboxes.items():
            if not checkbox.isChecked():
                continue
            spectra = self.reference_catalogues.spectra(cat)
            progress = QProgressDialog('Downloading spectra from catalog {}'.format(cat), 'Cancel', 0, len(spectra))
            progress.setWindowTitle('Downloading catalogs')
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            for index, spectrum in enumerate(spectra):
                progress.setValue(index)
                if progress.wasCanceled():
                    return;
                QApplication.instance().processEvents()
                self.reference_catalogues.fits(spectrum)