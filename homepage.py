from pyui.homepage import Ui_HomePage
from PyQt5.QtWidgets import QApplication
from pyspectrum_commons import *
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from qtcommons import QtCommons
from PyQt5.QtWidgets import QWidget, QToolBar
from PyQt5.QtCore import Qt, QObject, pyqtSignal

class HomePage(QWidget):
    import_image = pyqtSignal(str)
    calibrate = pyqtSignal(str)
    math = pyqtSignal(str)
    finish = pyqtSignal(str)

    def __init__(self, settings):
        QWidget.__init__(self)
        last_files_list = LastFilesList(settings)
        self.ui = Ui_HomePage()
        self.ui.setupUi(self)
        self.toolbar = QToolBar()
        welcome_text = "{} {}".format(QApplication.instance().applicationName(), QApplication.instance().applicationVersion())
        self.ui.welcome_label.setText(self.ui.welcome_label.text().format(welcome_text))
        file_action = QtCommons.addToolbarPopup(self.toolbar, 'File')
        file_action.menu().addAction(QIcon(':/image_20'), 'Import Image', lambda: open_file_sticky('Open FITS Image',FITS_IMG_EXTS, lambda f: self.import_image.emit(f[0]), settings, IMPORT_IMG ))
        file_action.menu().addAction(QIcon(':/plot_20'), 'Calibrate Spectrum', lambda: open_file_sticky('Open raw FITS Spectrum',FITS_EXTS, lambda f: self.calibrate.emit(f[0]), settings, RAW_PROFILE, [IMPORT_IMG] ))
        file_action.menu().addAction(QIcon(':/math_20'), 'Spectra Math', lambda: self.math.emit(None) )
        file_action.menu().addAction(QIcon(':/done_20'), 'Finish Spectrum', lambda: open_file_sticky('Open FITS Spectrum',FITS_EXTS, lambda f: self.finish.emit(f[0]), settings, CALIBRATED_PROFILE, [RAW_PROFILE,IMPORT_IMG] ))
        self.recent_raw_model = QStandardItemModel()
        self.recent_calibrated_model = QStandardItemModel()
        self.ui.recent_raw_list.setModel(self.recent_raw_model)
        self.ui.recent_calibrated_list.setModel(self.recent_calibrated_model)
        LastFilesList.instance().files_changed.connect(self.__populate_lists)
        selected_path = lambda model, view: model.item(view.selectionModel().selectedRows()[0].row()).data()
        button_enable = lambda view, button: view.selectionModel().selectionChanged.connect(lambda sel, desel: button.setEnabled(len(sel.indexes() )) )
        
        button_enable(self.ui.recent_raw_list, self.ui.calibrate)
        button_enable(self.ui.recent_calibrated_list, self.ui.math)
        button_enable(self.ui.recent_calibrated_list, self.ui.finish)
        self.ui.calibrate.clicked.connect(lambda: self.calibrate.emit(selected_path(self.recent_raw_model, self.ui.recent_raw_list)))
        self.ui.math.clicked.connect(lambda: self.math.emit(selected_path(self.recent_calibrated_model, self.ui.recent_calibrated_list)))
        self.ui.finish.clicked.connect(lambda: self.finish.emit(selected_path(self.recent_calibrated_model, self.ui.recent_calibrated_list)))
        self.__populate_lists()

    def __populate_lists(self):
        for key, model in [(RAW_PROFILE, self.recent_raw_model), (CALIBRATED_PROFILE, self.recent_calibrated_model)]:
            model.clear()
            for name, dir, path in LastFilesList.instance().last_files(key):
                model.setHorizontalHeaderLabels(["File", "Directory"])
                item = QStandardItem(name)
                item.setData(path)
                model.appendRow([item, QStandardItem(dir)])