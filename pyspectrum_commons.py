from qtcommons import *
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog, QAction, QDoubleSpinBox
from PyQt5.QtGui import QIcon
from spectrum_trim_dialog import SpectrumTrimDialog
from pyui.notification import Ui_Notification

FITS_EXTS = "FITS Images (*.fit *.fits *.tfits *.fit.gz *.fits.gz *.tfits.gz)"
FITS_IMG_EXTS = "FITS Images (*.fit *.fits *.fit.gz *.fits.gz)"
PROJECT_FILES = "Project Files (*.json)"

IMPORT_IMG = "import_image"
RAW_PROFILE = "raw_profile"
EXPORT_IMAGES = "export_image"
CALIBRATED_PROFILE = "calibrated_profile"
REFERENCE = "reference_spectrum"
MATH_OPERATION = "math_operation"
PROJECTS = "projects"

from PyQt5.QtWidgets import QInputDialog

class Instances:
    MainWindow = None

class LastFilesList(QObject):
    files_changed = pyqtSignal()
    __instance = None
    def __init__(self, settings):
        QObject.__init__(self)
        if LastFilesList.__instance:
            raise RuntimeError('LastFilesList should be created only once')
        self.settings = settings
        LastFilesList.__instance = self
        
    def __files_list(self, key):
        return self.settings.value("{}_last_files".format(key), [])
    
    def add_file(self, key, path):
        last_files = self.__files_list(key)
        last_files.insert(0, path)
        last_files = [x for i, x in enumerate(last_files) if last_files.index(x) == i][0:10]
        self.settings.setValue("{}_last_files".format(key), last_files)
        self.files_changed.emit()
    
    def last_files(self, key):
        return [(os.path.basename(v), os.path.dirname(v), v) for v in self.__files_list(key)]
    
    def instance():
        return LastFilesList.__instance

def spectrum_trim_dialog(spectrum, direction, axes, redraw, parent):
    dialog = SpectrumTrimDialog(spectrum, direction, axes, redraw, parent)
    dialog.setAttribute( Qt.WA_DeleteOnClose , False)
    dialog.show()

    
def save_path(settings, key_name, file_obj, on_ok):
    settings.setValue("{}_last_directory".format(key_name), os.path.dirname(file_obj[0]))
    LastFilesList.instance().add_file(key_name, file_obj[0])
    on_ok(file_obj)

def saved_directory(key_name, other_keys, default_path, settings):
    key_name = "{}_last_directory".format(key_name)
    if settings.contains(key_name):
        return settings.value(key_name, type=str)
    for key in other_keys:
        if settings.contains(key):
            return settings.value(key, type=str)
    return default_path if default_path else QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)

def save_file_sticky(title, file_types, on_ok, settings, key_name, other_keys=[], default_path=None, parent=None):
    directory = saved_directory(key_name, other_keys, default_path, settings)
    QtCommons.save_file(title, file_types, lambda f: save_path(settings, key_name, f, on_ok), directory, parent)
        
def open_file_sticky(title, file_types, on_ok, settings, key_name, other_keys=[], default_path=None, parent=None):
    directory = saved_directory(key_name, other_keys, default_path, settings)
    QtCommons.open_file(title, file_types, lambda f: save_path(settings, key_name, f, on_ok), directory, parent)
        
def open_directory_sticky(title, on_ok, settings, key_name, other_keys=[], default_path=None, parent=None):
    directory = saved_directory(key_name, other_keys, default_path, settings)
    QtCommons.open_dir(title, lambda f: save_path(settings, key_name, f, on_ok), dir=directory, parent=parent)
    
def open_files_sticky(title, file_types, on_ok, settings, key_name, other_keys=[], default_path=None, parent=None):
    directory = saved_directory(key_name, other_keys, default_path, settings)
    QtCommons.open_files(title, file_types, lambda f: save_path(settings, key_name, f, on_ok), directory, parent)


    
def Notification(text, title=None, parent=None, type='info', timeout=None):
                                        # or BypassWindowManagerHint /FramelessWindowHint
    print(Instances.MainWindow)
    popup = QWidget(Instances.MainWindow, Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    ui = Ui_Notification()
    ui.setupUi(popup)
    ui.text.setText(text)
    ui.title.setText(title)
    ui.close.clicked.connect(popup.deleteLater)
    ui.widget.setStyleSheet({
        'info': 'background-color: rgba(126, 214, 255, 220);',
        'warning': 'background-color: rgba(255, 212, 94, 220);',
        'error': 'background-color: rgba(255, 45, 45, 220);',
        'success': 'background-color: rgba(150, 255, 186, 220);',
        }[type])
    popup.move(QApplication.desktop().screen().rect().center() - popup.rect().center())
    popup.setAttribute(Qt.WA_TranslucentBackground, True)
    if timeout:
        timer = QTimer(popup)
        timer.timeout.connect(popup.deleteLater)
        timer.start(timeout*1000)
    popup.show()
    return popup