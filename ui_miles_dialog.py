# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'miles_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MilesDialog(object):
    def setupUi(self, MilesDialog):
        MilesDialog.setObjectName("MilesDialog")
        MilesDialog.resize(344, 255)
        self.gridLayout = QtWidgets.QGridLayout(MilesDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(MilesDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.type_filter = QtWidgets.QComboBox(MilesDialog)
        self.type_filter.setEditable(True)
        self.type_filter.setObjectName("type_filter")
        self.gridLayout.addWidget(self.type_filter, 0, 1, 1, 1)
        self.miles_entries = QtWidgets.QTableView(MilesDialog)
        self.miles_entries.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.miles_entries.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.miles_entries.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.miles_entries.setObjectName("miles_entries")
        self.miles_entries.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.miles_entries, 1, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(MilesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Open)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(MilesDialog)
        self.buttonBox.accepted.connect(MilesDialog.accept)
        self.buttonBox.rejected.connect(MilesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MilesDialog)

    def retranslateUi(self, MilesDialog):
        _translate = QtCore.QCoreApplication.translate
        MilesDialog.setWindowTitle(_translate("MilesDialog", "MILES Library"))
        self.label.setText(_translate("MilesDialog", "Filter by type"))

