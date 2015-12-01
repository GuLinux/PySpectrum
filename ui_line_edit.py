# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'line_edit.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LineEdit(object):
    def setupUi(self, LineEdit):
        LineEdit.setObjectName("LineEdit")
        LineEdit.resize(389, 150)
        self.gridLayout = QtWidgets.QGridLayout(LineEdit)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(LineEdit)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.line_text = QtWidgets.QLineEdit(LineEdit)
        self.line_text.setObjectName("line_text")
        self.gridLayout.addWidget(self.line_text, 0, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 2)
        self.reset_default = QtWidgets.QPushButton(LineEdit)
        self.reset_default.setObjectName("reset_default")
        self.gridLayout.addWidget(self.reset_default, 0, 3, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(LineEdit)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 4)
        self.show_lambda = QtWidgets.QCheckBox(LineEdit)
        self.show_lambda.setObjectName("show_lambda")
        self.gridLayout.addWidget(self.show_lambda, 1, 0, 1, 4)
        self.remove_line = QtWidgets.QPushButton(LineEdit)
        self.remove_line.setObjectName("remove_line")
        self.gridLayout.addWidget(self.remove_line, 2, 3, 1, 1)

        self.retranslateUi(LineEdit)
        self.buttonBox.accepted.connect(LineEdit.accept)
        self.buttonBox.rejected.connect(LineEdit.reject)
        QtCore.QMetaObject.connectSlotsByName(LineEdit)

    def retranslateUi(self, LineEdit):
        _translate = QtCore.QCoreApplication.translate
        LineEdit.setWindowTitle(_translate("LineEdit", "Dialog"))
        self.label.setText(_translate("LineEdit", "Text"))
        self.reset_default.setText(_translate("LineEdit", "Default"))
        self.show_lambda.setText(_translate("LineEdit", "Show wavelength"))
        self.remove_line.setText(_translate("LineEdit", "Remove line"))

