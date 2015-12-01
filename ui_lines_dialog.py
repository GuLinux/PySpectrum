# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lines_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LinesDialog(object):
    def setupUi(self, LinesDialog):
        LinesDialog.setObjectName("LinesDialog")
        LinesDialog.resize(444, 326)
        self.gridLayout_2 = QtWidgets.QGridLayout(LinesDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(LinesDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 3, 2, 1, 6)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 6, 2, 1)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 0, 2, 2)
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 3, 2, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout.addWidget(self.spinBox_2, 0, 7, 2, 1)
        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 0, 4, 2, 2)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.lines = QtWidgets.QTableView(LinesDialog)
        self.lines.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lines.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lines.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.lines.setObjectName("lines")
        self.lines.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_2.addWidget(self.lines, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(LinesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(LinesDialog)
        self.buttonBox.accepted.connect(LinesDialog.accept)
        self.buttonBox.rejected.connect(LinesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LinesDialog)

    def retranslateUi(self, LinesDialog):
        _translate = QtCore.QCoreApplication.translate
        LinesDialog.setWindowTitle(_translate("LinesDialog", "Dialog"))
        self.groupBox.setTitle(_translate("LinesDialog", "Filters"))
        self.label_3.setText(_translate("LinesDialog", "to"))
        self.checkBox.setText(_translate("LinesDialog", "Wavelength range"))
        self.checkBox_2.setText(_translate("LinesDialog", "Element"))
        self.label_2.setText(_translate("LinesDialog", "from"))

