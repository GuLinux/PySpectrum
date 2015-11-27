# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calibrate_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Calibrate(object):
    def setupUi(self, Calibrate):
        Calibrate.setObjectName("Calibrate")
        Calibrate.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Calibrate)
        self.gridLayout.setObjectName("gridLayout")
        self.second_point_pixel = QtWidgets.QDoubleSpinBox(Calibrate)
        self.second_point_pixel.setObjectName("second_point_pixel")
        self.gridLayout.addWidget(self.second_point_pixel, 6, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 72, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 1)
        self.second_point_lambda = QtWidgets.QDoubleSpinBox(Calibrate)
        self.second_point_lambda.setObjectName("second_point_lambda")
        self.gridLayout.addWidget(self.second_point_lambda, 6, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Calibrate)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Calibrate)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Calibrate)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.first_point_lambda = QtWidgets.QDoubleSpinBox(Calibrate)
        self.first_point_lambda.setObjectName("first_point_lambda")
        self.gridLayout.addWidget(self.first_point_lambda, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(Calibrate)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Calibrate)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 2)
        self.first_point_pixel = QtWidgets.QDoubleSpinBox(Calibrate)
        self.first_point_pixel.setObjectName("first_point_pixel")
        self.gridLayout.addWidget(self.first_point_pixel, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Calibrate)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(Calibrate)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Calibrate)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 1, 1, 1)

        self.retranslateUi(Calibrate)
        self.buttonBox.accepted.connect(Calibrate.accept)
        self.buttonBox.rejected.connect(Calibrate.reject)
        QtCore.QMetaObject.connectSlotsByName(Calibrate)

    def retranslateUi(self, Calibrate):
        _translate = QtCore.QCoreApplication.translate
        Calibrate.setWindowTitle(_translate("Calibrate", "Calibrate"))
        self.label_4.setText(_translate("Calibrate", "Pixel"))
        self.label_3.setText(_translate("Calibrate", "Second point"))
        self.label_2.setText(_translate("Calibrate", "First point"))
        self.label.setText(_translate("Calibrate", "Linear Calibration"))
        self.label_5.setText(_translate("Calibrate", "Lambda (Å)"))
        self.label_6.setText(_translate("Calibrate", "Pixel"))
        self.label_7.setText(_translate("Calibrate", "Lambda (Å)"))

