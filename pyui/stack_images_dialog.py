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
        StackImagesDialog.resize(798, 671)
        self.gridLayout = QtWidgets.QGridLayout(StackImagesDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.add = QtWidgets.QPushButton(StackImagesDialog)
        self.add.setObjectName("add")
        self.horizontalLayout.addWidget(self.add)
        self.remove = QtWidgets.QPushButton(StackImagesDialog)
        self.remove.setEnabled(False)
        self.remove.setObjectName("remove")
        self.horizontalLayout.addWidget(self.remove)
        self.reference = QtWidgets.QPushButton(StackImagesDialog)
        self.reference.setEnabled(False)
        self.reference.setObjectName("reference")
        self.horizontalLayout.addWidget(self.reference)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.plot = QtWidgets.QWidget(StackImagesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setObjectName("plot")
        self.gridLayout.addWidget(self.plot, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(StackImagesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.files = QtWidgets.QTableView(StackImagesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.files.sizePolicy().hasHeightForWidth())
        self.files.setSizePolicy(sizePolicy)
        self.files.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.files.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.files.setObjectName("files")
        self.gridLayout.addWidget(self.files, 1, 1, 1, 1)

        self.retranslateUi(StackImagesDialog)
        self.buttonBox.accepted.connect(StackImagesDialog.accept)
        self.buttonBox.rejected.connect(StackImagesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StackImagesDialog)

    def retranslateUi(self, StackImagesDialog):
        _translate = QtCore.QCoreApplication.translate
        StackImagesDialog.setWindowTitle(_translate("StackImagesDialog", "Dialog"))
        self.add.setText(_translate("StackImagesDialog", "Add"))
        self.remove.setText(_translate("StackImagesDialog", "Remove"))
        self.reference.setText(_translate("StackImagesDialog", "Set Reference"))

