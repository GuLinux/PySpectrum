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
        LineEdit.resize(389, 187)
        self.gridLayout = QtWidgets.QGridLayout(LineEdit)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(LineEdit)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.line_text = QtWidgets.QLineEdit(LineEdit)
        self.line_text.setObjectName("line_text")
        self.gridLayout.addWidget(self.line_text, 0, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 2)
        self.reset_default_text = QtWidgets.QPushButton(LineEdit)
        self.reset_default_text.setObjectName("reset_default_text")
        self.gridLayout.addWidget(self.reset_default_text, 0, 3, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(LineEdit)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 4)
        self.remove_line = QtWidgets.QPushButton(LineEdit)
        self.remove_line.setObjectName("remove_line")
        self.gridLayout.addWidget(self.remove_line, 3, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(LineEdit)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.reset_default_size = QtWidgets.QPushButton(LineEdit)
        self.reset_default_size.setObjectName("reset_default_size")
        self.gridLayout.addWidget(self.reset_default_size, 1, 3, 1, 1)
        self.text_size = QtWidgets.QDoubleSpinBox(LineEdit)
        self.text_size.setDecimals(1)
        self.text_size.setObjectName("text_size")
        self.gridLayout.addWidget(self.text_size, 1, 1, 1, 2)
        self.show_lambda = QtWidgets.QCheckBox(LineEdit)
        self.show_lambda.setObjectName("show_lambda")
        self.gridLayout.addWidget(self.show_lambda, 2, 1, 1, 3)
        self.wavelength = QtWidgets.QLabel(LineEdit)
        self.wavelength.setObjectName("wavelength")
        self.gridLayout.addWidget(self.wavelength, 2, 0, 1, 1)

        self.retranslateUi(LineEdit)
        self.buttonBox.accepted.connect(LineEdit.accept)
        self.buttonBox.rejected.connect(LineEdit.reject)
        QtCore.QMetaObject.connectSlotsByName(LineEdit)

    def retranslateUi(self, LineEdit):
        _translate = QtCore.QCoreApplication.translate
        LineEdit.setWindowTitle(_translate("LineEdit", "Edit Line Properties"))
        self.label.setText(_translate("LineEdit", "Text"))
        self.reset_default_text.setText(_translate("LineEdit", "Default"))
        self.remove_line.setText(_translate("LineEdit", "Remove line"))
        self.label_2.setText(_translate("LineEdit", "Size"))
        self.reset_default_size.setText(_translate("LineEdit", "Default"))
        self.show_lambda.setText(_translate("LineEdit", "Show wavelength"))
        self.wavelength.setText(_translate("LineEdit", "TextLabel"))

