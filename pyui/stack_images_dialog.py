# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/stack_images_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StackImagesDialog(object):
    def setupUi(self, StackImagesDialog):
        StackImagesDialog.setObjectName("StackImagesDialog")
        StackImagesDialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(StackImagesDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.plot = QtWidgets.QWidget(StackImagesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setObjectName("plot")
        self.gridLayout.addWidget(self.plot, 0, 0, 1, 1)
        self.files = QtWidgets.QTableWidget(StackImagesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.files.sizePolicy().hasHeightForWidth())
        self.files.setSizePolicy(sizePolicy)
        self.files.setObjectName("files")
        self.files.setColumnCount(0)
        self.files.setRowCount(0)
        self.gridLayout.addWidget(self.files, 0, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(StackImagesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.retranslateUi(StackImagesDialog)
        self.buttonBox.accepted.connect(StackImagesDialog.accept)
        self.buttonBox.rejected.connect(StackImagesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StackImagesDialog)

    def retranslateUi(self, StackImagesDialog):
        _translate = QtCore.QCoreApplication.translate
        StackImagesDialog.setWindowTitle(_translate("StackImagesDialog", "Dialog"))

