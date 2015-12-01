# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reference_spectra_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ReferenceSpectraDialog(object):
    def setupUi(self, ReferenceSpectraDialog):
        ReferenceSpectraDialog.setObjectName("ReferenceSpectraDialog")
        ReferenceSpectraDialog.resize(344, 255)
        self.gridLayout = QtWidgets.QGridLayout(ReferenceSpectraDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(ReferenceSpectraDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.catalogue = QtWidgets.QComboBox(ReferenceSpectraDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.catalogue.sizePolicy().hasHeightForWidth())
        self.catalogue.setSizePolicy(sizePolicy)
        self.catalogue.setObjectName("catalogue")
        self.gridLayout.addWidget(self.catalogue, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(ReferenceSpectraDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.type_filter = QtWidgets.QComboBox(ReferenceSpectraDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type_filter.sizePolicy().hasHeightForWidth())
        self.type_filter.setSizePolicy(sizePolicy)
        self.type_filter.setEditable(True)
        self.type_filter.setObjectName("type_filter")
        self.gridLayout.addWidget(self.type_filter, 1, 1, 1, 1)
        self.entries = QtWidgets.QTableView(ReferenceSpectraDialog)
        self.entries.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.entries.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.entries.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.entries.setObjectName("entries")
        self.entries.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.entries, 2, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(ReferenceSpectraDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Open)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(ReferenceSpectraDialog)
        self.buttonBox.accepted.connect(ReferenceSpectraDialog.accept)
        self.buttonBox.rejected.connect(ReferenceSpectraDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReferenceSpectraDialog)

    def retranslateUi(self, ReferenceSpectraDialog):
        _translate = QtCore.QCoreApplication.translate
        ReferenceSpectraDialog.setWindowTitle(_translate("ReferenceSpectraDialog", "Reference Spectra Library"))
        self.label_2.setText(_translate("ReferenceSpectraDialog", "Catalog"))
        self.label.setText(_translate("ReferenceSpectraDialog", "Filter by type"))

