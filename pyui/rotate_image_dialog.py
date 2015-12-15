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
        RotateImageDialog.resize(356, 161)
        self.gridLayout = QtWidgets.QGridLayout(RotateImageDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.rotate_spinbox = QtWidgets.QDoubleSpinBox(RotateImageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rotate_spinbox.sizePolicy().hasHeightForWidth())
        self.rotate_spinbox.setSizePolicy(sizePolicy)
        self.rotate_spinbox.setDecimals(5)
        self.rotate_spinbox.setMinimum(-165.0)
        self.rotate_spinbox.setMaximum(360.0)
        self.rotate_spinbox.setSingleStep(0.001)
        self.rotate_spinbox.setObjectName("rotate_spinbox")
        self.gridLayout.addWidget(self.rotate_spinbox, 1, 0, 1, 1)
        self.rotate_auto = QtWidgets.QPushButton(RotateImageDialog)
        self.rotate_auto.setObjectName("rotate_auto")
        self.gridLayout.addWidget(self.rotate_auto, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(RotateImageDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.rotate_mirror = QtWidgets.QPushButton(RotateImageDialog)
        self.rotate_mirror.setObjectName("rotate_mirror")
        self.gridLayout.addWidget(self.rotate_mirror, 1, 2, 1, 1)
        self.bb = QtWidgets.QDialogButtonBox(RotateImageDialog)
        self.bb.setOrientation(QtCore.Qt.Horizontal)
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Close)
        self.bb.setObjectName("bb")
        self.gridLayout.addWidget(self.bb, 5, 0, 1, 3)
        self.degrees_slider = QtWidgets.QSlider(RotateImageDialog)
        self.degrees_slider.setMaximum(360000)
        self.degrees_slider.setSingleStep(1)
        self.degrees_slider.setOrientation(QtCore.Qt.Horizontal)
        self.degrees_slider.setObjectName("degrees_slider")
        self.gridLayout.addWidget(self.degrees_slider, 3, 0, 1, 3)
        self.rotation_info = QtWidgets.QLabel(RotateImageDialog)
        self.rotation_info.setText("")
        self.rotation_info.setObjectName("rotation_info")
        self.gridLayout.addWidget(self.rotation_info, 4, 0, 1, 3)

        self.retranslateUi(RotateImageDialog)
        self.bb.accepted.connect(RotateImageDialog.accept)
        self.bb.rejected.connect(RotateImageDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RotateImageDialog)

    def retranslateUi(self, RotateImageDialog):
        _translate = QtCore.QCoreApplication.translate
        RotateImageDialog.setWindowTitle(_translate("RotateImageDialog", "Rotate Image..."))
        self.rotate_auto.setText(_translate("RotateImageDialog", "Auto"))
        self.label.setText(_translate("RotateImageDialog", "Enter degrees for image rotation"))
        self.rotate_mirror.setText(_translate("RotateImageDialog", "Mirror"))

