# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/finish_spectrum.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


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
