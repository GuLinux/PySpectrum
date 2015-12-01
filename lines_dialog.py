from ui_lines_dialog import Ui_LinesDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QSortFilterProxyModel, QSettings, QByteArray

import sqlite3

class LinesDialog(QDialog):
    lines = pyqtSignal(list)
    
    def __element_item(element):
        item = QStandardItem("{} ({})".format(element[2], element[1]) if element[1] else element[2] )
        item.setData({'z': element[0], 'code': element[1], 'name': element[2]})
        return item
    
    def __init__(self, database, settings, plot_widget, axes = None):
        super(LinesDialog, self).__init__()
        self.axes = axes if axes else plot_widget.axes
        self.database = database
        self.plot_widget = plot_widget
        self.settings = settings
        self.ui = Ui_LinesDialog()
        self.ui.setupUi(self)
        self.restoreGeometry(self.settings.value('pick_lines_geometry', QByteArray()))
        self.model = QStandardItemModel()
        self.elements_model = QStandardItemModel()
        self.ui.lines.setModel(self.model)
        self.ui.elements.setModel(self.elements_model)
        c = self.database.cursor()
        self.elements_model.appendRow(LinesDialog.__element_item([0, '', 'All']))
        elements = c.execute("SELECT z, code, name FROM elements ORDER BY z ASC")
        for element in elements:
            self.elements_model.appendRow(LinesDialog.__element_item(element))
        
        self.ui.elements.currentTextChanged.connect(lambda t: self.populate())
        self.ui.lambda_from.editingFinished.connect(self.populate)
        self.ui.lambda_to.editingFinished.connect(self.populate)
        self.accepted.connect(self.collect_selected_lines)
        self.populate()
        self.ui.pick_wavelengths.clicked.connect(self.pick_wavelengths_clicked)
        
    def pick_wavelengths_clicked(self):
        self.plot_widget.add_span_selector("pick_lines_lambda", self.picked_wavelengths, axes=self.axes, direction='horizontal')
        self.lower()
        
    def closeEvent(self, ev):
        self.settings.setValue('pick_lines_geometry', self.saveGeometry())
        QDialog.closeEvent(self, ev)
        
    def picked_wavelengths(self, start, end):
        self.raise_()
        self.ui.lambda_from.setValue(start)
        self.ui.lambda_to.setValue(end)
        self.plot_widget.rm_element("pick_lines_lambda")
        self.populate()

    def collect_selected_lines(self):
        selected_rows = self.ui.lines.selectionModel().selectedRows()
        if selected_rows:
            self.lines.emit([self.model.itemFromIndex(i).data() for i in selected_rows])
        
    def populate(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Lambda', 'Element', 'Atomic number', 'Ionization', 'Stellar spectral types'])
        c = self.database.cursor()
        query = "SELECT lambda, Element, Z, Ion, SpTypes from spectral_lines WHERE {} ORDER BY lambda ASC;"
        conditions = ['(1 = 1)']
        
        element = self.elements_model.item(self.ui.elements.currentIndex()).data()
        if element['z']:
            conditions.append("(Z = {})".format(element['z']))
        
        if self.ui.lambda_from.value() > 0:
            conditions.append("(Lambda >= {})".format(self.ui.lambda_from.value()))
        if self.ui.lambda_to.value() > 0:
            conditions.append("(Lambda <= {})".format(self.ui.lambda_to.value()))
        
        for row in c.execute(query.format(" AND ".join(conditions))):
            first_item = QStandardItem("{}".format(row[0]))
            first_item.setData({'lambda': row[0], 'name': row[1], 'z': row[2]})
            self.model.appendRow( [
                first_item,
                QStandardItem(row[1]),
                QStandardItem("{}".format(row[2])),
                QStandardItem("{}".format(row[3])),
                QStandardItem(row[4])
                ])