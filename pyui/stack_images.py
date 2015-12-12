# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/stack_images.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StackImages(object):
    def setupUi(self, StackImages):
        StackImages.setObjectName("StackImages")
        StackImages.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(StackImages)
        self.gridLayout.setObjectName("gridLayout")
        self.plot = QtWidgets.QWidget(StackImages)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setObjectName("plot")
        self.gridLayout.addWidget(self.plot, 0, 1, 2, 1)
        self.files = QtWidgets.QTableView(StackImages)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.files.sizePolicy().hasHeightForWidth())
        self.files.setSizePolicy(sizePolicy)
        self.files.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.files.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.files.setObjectName("files")
        self.gridLayout.addWidget(self.files, 0, 0, 2, 1)

        self.retranslateUi(StackImages)
        QtCore.QMetaObject.connectSlotsByName(StackImages)

    def retranslateUi(self, StackImages):
        _translate = QtCore.QCoreApplication.translate
        StackImages.setWindowTitle(_translate("StackImages", "Form"))

