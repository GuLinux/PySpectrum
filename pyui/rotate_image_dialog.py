# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/rotate_image_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RotateImageDialog(object):
    def setupUi(self, RotateImageDialog):
        RotateImageDialog.setObjectName("RotateImageDialog")
        RotateImageDialog.resize(356, 137)
        self.gridLayout = QtWidgets.QGridLayout(RotateImageDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.rotate_spinbox = QtWidgets.QDoubleSpinBox(RotateImageDialog)
        self.rotate_spinbox.setDecimals(3)
        self.rotate_spinbox.setMaximum(360.0)
        self.rotate_spinbox.setSingleStep(0.001)
        self.rotate_spinbox.setObjectName("rotate_spinbox")
        self.gridLayout.addWidget(self.rotate_spinbox, 1, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.bb = QtWidgets.QDialogButtonBox(RotateImageDialog)
        self.bb.setOrientation(QtCore.Qt.Horizontal)
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Close)
        self.bb.setObjectName("bb")
        self.gridLayout.addWidget(self.bb, 4, 0, 1, 2)
        self.label = QtWidgets.QLabel(RotateImageDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.degrees_slider = QtWidgets.QSlider(RotateImageDialog)
        self.degrees_slider.setMaximum(360000)
        self.degrees_slider.setSingleStep(1)
        self.degrees_slider.setOrientation(QtCore.Qt.Horizontal)
        self.degrees_slider.setObjectName("degrees_slider")
        self.gridLayout.addWidget(self.degrees_slider, 3, 0, 1, 1)

        self.retranslateUi(RotateImageDialog)
        self.bb.accepted.connect(RotateImageDialog.accept)
        self.bb.rejected.connect(RotateImageDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RotateImageDialog)

    def retranslateUi(self, RotateImageDialog):
        _translate = QtCore.QCoreApplication.translate
        RotateImageDialog.setWindowTitle(_translate("RotateImageDialog", "Rotate Image..."))
        self.label.setText(_translate("RotateImageDialog", "Enter degrees for image rotation"))

