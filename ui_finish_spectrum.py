# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'finish_spectrum.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FinishSpectrum(object):
    def setupUi(self, FinishSpectrum):
        FinishSpectrum.setObjectName("FinishSpectrum")
        FinishSpectrum.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(FinishSpectrum)
        self.gridLayout.setObjectName("gridLayout")
        self.plot = QtWidgets.QWidget(FinishSpectrum)
        self.plot.setObjectName("plot")
        self.gridLayout.addWidget(self.plot, 0, 0, 1, 1)

        self.retranslateUi(FinishSpectrum)
        QtCore.QMetaObject.connectSlotsByName(FinishSpectrum)

    def retranslateUi(self, FinishSpectrum):
        _translate = QtCore.QCoreApplication.translate
        FinishSpectrum.setWindowTitle(_translate("FinishSpectrum", "Form"))

