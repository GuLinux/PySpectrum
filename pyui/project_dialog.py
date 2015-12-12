# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/project_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProjectDialog(object):
    def setupUi(self, ProjectDialog):
        ProjectDialog.setObjectName("ProjectDialog")
        ProjectDialog.resize(361, 260)
        self.gridLayout = QtWidgets.QGridLayout(ProjectDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(ProjectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 2)
        self.label = QtWidgets.QLabel(ProjectDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtWidgets.QLineEdit(ProjectDialog)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(ProjectDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.path = QtWidgets.QLineEdit(ProjectDialog)
        self.path.setObjectName("path")
        self.gridLayout.addWidget(self.path, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(ProjectDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.date = QtWidgets.QDateEdit(ProjectDialog)
        self.date.setCalendarPopup(True)
        self.date.setObjectName("date")
        self.gridLayout.addWidget(self.date, 4, 1, 1, 1)
        self.observer = QtWidgets.QLineEdit(ProjectDialog)
        self.observer.setObjectName("observer")
        self.gridLayout.addWidget(self.observer, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(ProjectDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.equipment = QtWidgets.QLineEdit(ProjectDialog)
        self.equipment.setObjectName("equipment")
        self.gridLayout.addWidget(self.equipment, 5, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(ProjectDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(ProjectDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.position = QtWidgets.QLineEdit(ProjectDialog)
        self.position.setObjectName("position")
        self.gridLayout.addWidget(self.position, 2, 1, 1, 1)

        self.retranslateUi(ProjectDialog)
        self.buttonBox.accepted.connect(ProjectDialog.accept)
        self.buttonBox.rejected.connect(ProjectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ProjectDialog)

    def retranslateUi(self, ProjectDialog):
        _translate = QtCore.QCoreApplication.translate
        ProjectDialog.setWindowTitle(_translate("ProjectDialog", "Project"))
        self.label.setText(_translate("ProjectDialog", "Project Name"))
        self.label_2.setText(_translate("ProjectDialog", "Directory"))
        self.label_3.setText(_translate("ProjectDialog", "Observer"))
        self.label_4.setText(_translate("ProjectDialog", "Date"))
        self.label_5.setText(_translate("ProjectDialog", "Equipment"))
        self.label_6.setText(_translate("ProjectDialog", "Position"))

