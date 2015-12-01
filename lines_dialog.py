from ui_lines_dialog import Ui_LinesDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QSortFilterProxyModel
import sqlite3

class LinesDialog(QDialog):
    def __init__(self):
        super(LinesDialog, self).__init__()
        self.ui = Ui_LinesDialog()
        self.ui.setupUi(self)
        self.model = QStandardItemModel()
        self.ui.lines.setModel(self.model)
        conn = sqlite3.connect('data/pyspectrum.db')
        c = conn.cursor()
        for row in c.execute("SELECT lambda, Element, Z, Ion, SpTypes from spectral_lines;"):
            self.model.appendRow( [
                QStandardItem("{}".format(row[0])),
                QStandardItem(row[1]),
                QStandardItem("{}".format(row[2])),
                QStandardItem("{}".format(row[3])),
                QStandardItem(row[4])
                ])
        self.model.setHorizontalHeaderLabels(['Lambda', 'Element', 'Atomic number', 'Ionization', 'Stellar spectral types'])