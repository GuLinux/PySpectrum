from ui_lines_dialog import Ui_LinesDialog
from astropy.io import fits
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QSortFilterProxyModel

class LinesDialog(QDialog):
    def __init__(self):
        super(LinesDialog, self).__init__()
        self.ui = Ui_LinesDialog()
        self.ui.setupUi(self)
        self.model = QStandardItemModel()
        self.ui.lines.setModel(self.model)
        fits_file = fits.open('data/lines.fit.gz')
        tbdata = fits_file[1]
        for row in tbdata.data:
            self.model.appendRow( [
                QStandardItem("{}".format(row['lambda'])),
                QStandardItem(row['Element']),
                QStandardItem("{}".format(row['Z'])),
                QStandardItem("{}".format(row['Ion'])),
                QStandardItem(row['SpTypes'])
                ])
        self.model.setHorizontalHeaderLabels(['Lambda', 'Element', 'Atomic number', 'Ionization', 'Stellar spectral types'])