# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/spectrum_trim_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SpectrumTrimDialog(object):
    def setupUi(self, SpectrumTrimDialog):
        SpectrumTrimDialog.setObjectName("SpectrumTrimDialog")
        SpectrumTrimDialog.resize(344, 106)
        self.gridLayout = QtWidgets.QGridLayout(SpectrumTrimDialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(SpectrumTrimDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.wavelength = QtWidgets.QDoubleSpinBox(SpectrumTrimDialog)
        self.wavelength.setObjectName("wavelength")
        self.gridLayout.addWidget(self.wavelength, 1, 0, 1, 2)
        self.label = QtWidgets.QLabel(SpectrumTrimDialog)
        self.label.setMinimumSize(QtCore.QSize(332, 0))
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.retranslateUi(SpectrumTrimDialog)
        QtCore.QMetaObject.connectSlotsByName(SpectrumTrimDialog)

    def retranslateUi(self, SpectrumTrimDialog):
        _translate = QtCore.QCoreApplication.translate
        SpectrumTrimDialog.setWindowTitle(_translate("SpectrumTrimDialog", "Delete Points"))
        self.label.setText(_translate("SpectrumTrimDialog", "Enter wavelength for data trimming, or double-click the plot to automatically select wavelength"))

