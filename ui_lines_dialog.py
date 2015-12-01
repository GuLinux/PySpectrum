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
        LinesDialog.resize(682, 523)
        self.gridLayout_2 = QtWidgets.QGridLayout(LinesDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(LinesDialog)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.elements = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.elements.sizePolicy().hasHeightForWidth())
        self.elements.setSizePolicy(sizePolicy)
        self.elements.setObjectName("elements")
        self.horizontalLayout.addWidget(self.elements)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lambda_from = QtWidgets.QSpinBox(self.groupBox)
        self.lambda_from.setMaximum(9999999)
        self.lambda_from.setObjectName("lambda_from")
        self.horizontalLayout.addWidget(self.lambda_from)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.lambda_to = QtWidgets.QSpinBox(self.groupBox)
        self.lambda_to.setMaximum(9999999)
        self.lambda_to.setObjectName("lambda_to")
        self.horizontalLayout.addWidget(self.lambda_to)
        self.pick_wavelengths = QtWidgets.QToolButton(self.groupBox)
        self.pick_wavelengths.setObjectName("pick_wavelengths")
        self.horizontalLayout.addWidget(self.pick_wavelengths)
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
        self.label.setText(_translate("LinesDialog", "Element"))
        self.label_2.setText(_translate("LinesDialog", "Wavelength"))
        self.label_3.setText(_translate("LinesDialog", "to"))
        self.pick_wavelengths.setText(_translate("LinesDialog", "..."))

