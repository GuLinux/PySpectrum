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
        HomePage.resize(859, 585)
        self.gridLayout = QtWidgets.QGridLayout(HomePage)
        self.gridLayout.setObjectName("gridLayout")
        self.welcome_label = QtWidgets.QLabel(HomePage)
        self.welcome_label.setObjectName("welcome_label")
        self.gridLayout.addWidget(self.welcome_label, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(HomePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(HomePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(HomePage)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.import_image = QtWidgets.QPushButton(self.groupBox_3)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image_20.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.import_image.setIcon(icon)
        self.import_image.setFlat(True)
        self.import_image.setObjectName("import_image")
        self.horizontalLayout.addWidget(self.import_image)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.calibrate = QtWidgets.QPushButton(self.groupBox_3)
        self.calibrate.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/plot_20.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.calibrate.setIcon(icon1)
        self.calibrate.setFlat(True)
        self.calibrate.setObjectName("calibrate")
        self.horizontalLayout.addWidget(self.calibrate)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.recent_raw_list = QtWidgets.QTableView(self.groupBox_3)
        self.recent_raw_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.recent_raw_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.recent_raw_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.recent_raw_list.setObjectName("recent_raw_list")
        self.recent_raw_list.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.recent_raw_list)
        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(HomePage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.math = QtWidgets.QPushButton(self.groupBox_2)
        self.math.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/math_20.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.math.setIcon(icon2)
        self.math.setFlat(True)
        self.math.setObjectName("math")
        self.horizontalLayout_2.addWidget(self.math)
        self.finish = QtWidgets.QPushButton(self.groupBox_2)
        self.finish.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/done_20.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.finish.setIcon(icon3)
        self.finish.setFlat(True)
        self.finish.setObjectName("finish")
        self.horizontalLayout_2.addWidget(self.finish)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.recent_calibrated_list = QtWidgets.QTableView(self.groupBox_2)
        self.recent_calibrated_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.recent_calibrated_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.recent_calibrated_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.recent_calibrated_list.setObjectName("recent_calibrated_list")
        self.recent_calibrated_list.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_3.addWidget(self.recent_calibrated_list)
        self.gridLayout.addWidget(self.groupBox_2, 2, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(HomePage)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.new_project = QtWidgets.QPushButton(self.groupBox)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/project_new_20.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.new_project.setIcon(icon4)
        self.new_project.setFlat(True)
        self.new_project.setObjectName("new_project")
        self.horizontalLayout_3.addWidget(self.new_project)
        self.pick_project = QtWidgets.QPushButton(self.groupBox)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/folder_open_20.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pick_project.setIcon(icon5)
        self.pick_project.setFlat(True)
        self.pick_project.setObjectName("pick_project")
        self.horizontalLayout_3.addWidget(self.pick_project)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.open_recent_project = QtWidgets.QPushButton(self.groupBox)
        self.open_recent_project.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/new_open_20.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.open_recent_project.setIcon(icon6)
        self.open_recent_project.setFlat(True)
        self.open_recent_project.setObjectName("open_recent_project")
        self.horizontalLayout_3.addWidget(self.open_recent_project)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.recent_projects = QtWidgets.QTableView(self.groupBox)
        self.recent_projects.setEnabled(True)
        self.recent_projects.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.recent_projects.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.recent_projects.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.recent_projects.setObjectName("recent_projects")
        self.recent_projects.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.recent_projects)
        self.gridLayout.addWidget(self.groupBox, 2, 2, 1, 1)
        self.download_catalogs = QtWidgets.QPushButton(HomePage)
        self.download_catalogs.setObjectName("download_catalogs")
        self.gridLayout.addWidget(self.download_catalogs, 3, 1, 1, 1)

        self.retranslateUi(HomePage)
        QtCore.QMetaObject.connectSlotsByName(HomePage)

    def retranslateUi(self, HomePage):
        _translate = QtCore.QCoreApplication.translate
        HomePage.setWindowTitle(_translate("HomePage", "Homepage"))
        self.welcome_label.setText(_translate("HomePage", "Welcome to {}."))
        self.label_4.setText(_translate("HomePage", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Files</span></p><p>You can open single files and process them directly.</p></body></html>"))
        self.label_5.setText(_translate("HomePage", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Projects</span></p><p>Use \'project\' mode to process all spectra shot with the same parameters (dispersion, rotation angle, location).</p><p>PySpectrum will automatically apply all these settings to all your files, saving you lots of processing time.</p></body></html>"))
        self.groupBox_3.setTitle(_translate("HomePage", "Recent Raw Spectra"))
        self.import_image.setText(_translate("HomePage", "Import"))
        self.calibrate.setText(_translate("HomePage", "Calibrate"))
        self.groupBox_2.setTitle(_translate("HomePage", "Recent Calibrated Spectra"))
        self.math.setText(_translate("HomePage", "Math"))
        self.finish.setText(_translate("HomePage", "Finish"))
        self.groupBox.setTitle(_translate("HomePage", "Recent Projects"))
        self.new_project.setText(_translate("HomePage", "New"))
        self.pick_project.setText(_translate("HomePage", "Open"))
        self.open_recent_project.setText(_translate("HomePage", "Load"))
        self.download_catalogs.setText(_translate("HomePage", "Download Catalogs..."))

import resources_rc
