FITS_EXTS = "FITS Images (*.fit *.fits *.tfits *.fit.gz *.fits.gz *.tfits.gz)"
FITS_IMG_EXTS = "FITS Images (*.fit *.fits *.fit.gz *.fits.gz)"
IMPORT_IMG_DIR = "import_image_last_directory"
RAW_PROFILE_DIR = "raw_profile_last_directory"
EXPORT_IMAGES_DIR = "export_image_last_directory"
CALIBRATED_PROFILE_DIR = "calibrated_profile_last_directory"
REFERENCE_DIR = "reference_spectrum_last_directory"
MATH_OPERATION_DIR = "math_operation_last_directory"

from PyQt5.QtWidgets import QInputDialog

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
    