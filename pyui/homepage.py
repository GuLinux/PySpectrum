# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/homepage.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HomePage(object):
    def setupUi(self, HomePage):
        HomePage.setObjectName("HomePage")
        HomePage.resize(565, 364)
        self.gridLayout = QtWidgets.QGridLayout(HomePage)
        self.gridLayout.setObjectName("gridLayout")
        self.welcome_label = QtWidgets.QLabel(HomePage)
        self.welcome_label.setObjectName("welcome_label")
        self.gridLayout.addWidget(self.welcome_label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(HomePage)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(HomePage)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.recent_raw_list = QtWidgets.QTableView(HomePage)
        self.recent_raw_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.recent_raw_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.recent_raw_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.recent_raw_list.setObjectName("recent_raw_list")
        self.recent_raw_list.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.recent_raw_list, 2, 0, 1, 1)
        self.recent_calibrated_list = QtWidgets.QTableView(HomePage)
        self.recent_calibrated_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.recent_calibrated_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.recent_calibrated_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.recent_calibrated_list.setObjectName("recent_calibrated_list")
        self.recent_calibrated_list.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.recent_calibrated_list, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.calibrate = QtWidgets.QPushButton(HomePage)
        self.calibrate.setEnabled(False)
        self.calibrate.setObjectName("calibrate")
        self.horizontalLayout.addWidget(self.calibrate)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.math = QtWidgets.QPushButton(HomePage)
        self.math.setEnabled(False)
        self.math.setObjectName("math")
        self.horizontalLayout_2.addWidget(self.math)
        self.finish = QtWidgets.QPushButton(HomePage)
        self.finish.setEnabled(False)
        self.finish.setObjectName("finish")
        self.horizontalLayout_2.addWidget(self.finish)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 1, 1, 1)
        self.download_catalogs = QtWidgets.QPushButton(HomePage)
        self.download_catalogs.setObjectName("download_catalogs")
        self.gridLayout.addWidget(self.download_catalogs, 4, 0, 1, 1)

        self.retranslateUi(HomePage)
        QtCore.QMetaObject.connectSlotsByName(HomePage)

    def retranslateUi(self, HomePage):
        _translate = QtCore.QCoreApplication.translate
        HomePage.setWindowTitle(_translate("HomePage", "Homepage"))
        self.welcome_label.setText(_translate("HomePage", "Welcome to {}."))
        self.label_2.setText(_translate("HomePage", "Recent Raw spectra"))
        self.label_3.setText(_translate("HomePage", "Recent Calibrated Spectra"))
        self.calibrate.setText(_translate("HomePage", "Calibrate"))
        self.math.setText(_translate("HomePage", "Math"))
        self.finish.setText(_translate("HomePage", "Finish"))
        self.download_catalogs.setText(_translate("HomePage", "Download Catalogs..."))

