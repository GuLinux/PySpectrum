FITS_EXTS = "FITS Images (*.fit *.fits *.tfits *.fit.gz *.fits.gz *.tfits.gz)"
FITS_IMG_EXTS = "FITS Images (*.fit *.fits *.fit.gz *.fits.gz)"

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
    