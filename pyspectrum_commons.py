from qtcommons import *
from PyQt5.QtCore import Qt, QObject, pyqtSignal

FITS_EXTS = "FITS Images (*.fit *.fits *.tfits *.fit.gz *.fits.gz *.tfits.gz)"
FITS_IMG_EXTS = "FITS Images (*.fit *.fits *.fit.gz *.fits.gz)"

IMPORT_IMG = "import_image"
RAW_PROFILE = "raw_profile"
EXPORT_IMAGES = "export_image"
CALIBRATED_PROFILE = "calibrated_profile"
REFERENCE = "reference_spectrum"
MATH_OPERATION = "math_operation"

from PyQt5.QtWidgets import QInputDialog

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

def spectrum_trim_dialog(spectrum, direction, axes, redraw):
    point = QInputDialog.getInt(None, 'Trim curve', 'Enter wavelength for trimming', spectrum.wavelengths[0] if direction == 'before' else spectrum.wavelengths[-1], spectrum.wavelengths[0], spectrum.wavelengths[-1])
    if not point[1]:
        return
    if direction == 'before':
        spectrum.cut(start=spectrum.wavelength_index(point[0]))
    else:
        spectrum.cut(end=spectrum.wavelength_index(point[0]))
        
    spectrum.normalize_to_max()
    redraw()
    
def __save_filepath_setting_wrapper(settings, key_name, file_obj, on_ok):
    settings.setValue("{}_last_directory".format(key_name), os.path.dirname(file_obj[0]))
    LastFilesList.instance().add_file(key_name, file_obj[0])
    on_ok(file_obj)

def __get_directory(key_name, other_keys, default_path, settings):
    key_name = "{}_last_directory".format(key_name)
    if settings.contains(key_name):
        return settings.value(key_name, type=str)
    for key in other_keys:
        if settings.contains(key):
            return settings.value(key, type=str)
    return default_path if default_path else QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)

def save_file_sticky(title, file_types, on_ok, settings, key_name, other_keys=[], default_path=None):
    directory = __get_directory(key_name, other_keys, default_path, settings)
    QtCommons.save_file(title, file_types, lambda f: __save_filepath_setting_wrapper(settings, key_name, f, on_ok), directory)
        
def open_file_sticky(title, file_types, on_ok, settings, key_name, other_keys=[], default_path=None):
    directory = __get_directory(key_name, other_keys, default_path, settings)
    QtCommons.open_file(title, file_types, lambda f: __save_filepath_setting_wrapper(settings, key_name, f, on_ok), directory)
