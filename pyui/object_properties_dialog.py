# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/object_properties_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ObjectPropertiesDialog(object):
    def setupUi(self, ObjectPropertiesDialog):
        ObjectPropertiesDialog.setObjectName("ObjectPropertiesDialog")
        ObjectPropertiesDialog.resize(444, 402)
        self.gridLayout = QtWidgets.QGridLayout(ObjectPropertiesDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(ObjectPropertiesDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 7, 0, 1, 1)
        self.sptype = QtWidgets.QLineEdit(ObjectPropertiesDialog)
        self.sptype.setObjectName("sptype")
        self.gridLayout.addWidget(self.sptype, 3, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(ObjectPropertiesDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.simbad = QtWidgets.QPushButton(ObjectPropertiesDialog)
        self.simbad.setObjectName("simbad")
        self.gridLayout.addWidget(self.simbad, 0, 2, 1, 1)
        self.equipment = QtWidgets.QLineEdit(ObjectPropertiesDialog)
        self.equipment.setObjectName("equipment")
        self.gridLayout.addWidget(self.equipment, 9, 1, 1, 2)
        self.dec = QtWidgets.QLineEdit(ObjectPropertiesDialog)
        self.dec.setObjectName("dec")
        self.gridLayout.addWidget(self.dec, 5, 1, 1, 2)
        self.type = QtWidgets.QLineEdit(ObjectPropertiesDialog)
        self.type.setObjectName("type")
        self.gridLayout.addWidget(self.type, 2, 1, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(ObjectPropertiesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 12, 0, 1, 3)
        self.ra = QtWidgets.QLineEdit(ObjectPropertiesDialog)
        self.ra.setObjectName("ra")
        self.gridLayout.addWidget(self.ra, 4, 1, 1, 2)
        self.date = QtWidgets.QDateTimeEdit(ObjectPropertiesDialog)
        self.date.setCalendarPopup(True)
        self.date.setObjectName("date")
        self.gridLayout.addWidget(self.date, 7, 1, 1, 2)
        self.observer = QtWidgets.QLineEdit(ObjectPropertiesDialog)
        self.observer.setObjectName("observer")
        self.gridLayout.addWidget(self.observer, 8, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(ObjectPropertiesDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(ObjectPropertiesDialog)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 9, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(ObjectPropertiesDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.label = QtWidgets.QLabel(ObjectPropertiesDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(ObjectPropertiesDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(ObjectPropertiesDialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 8, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(ObjectPropertiesDialog)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 11, 0, 1, 1)
        self.position = QtWidgets.QLineEdit(ObjectPropertiesDialog)
        self.position.setObjectName("position")
        self.gridLayout.addWidget(self.position, 11, 1, 1, 2)
        self.name = QtWidgets.QComboBox(ObjectPropertiesDialog)
        self.name.setEditable(True)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(ObjectPropertiesDialog)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.names = QtWidgets.QLineEdit(ObjectPropertiesDialog)
        self.names.setObjectName("names")
        self.gridLayout.addWidget(self.names, 1, 1, 1, 2)

        self.retranslateUi(ObjectPropertiesDialog)
        self.buttonBox.accepted.connect(ObjectPropertiesDialog.accept)
        self.buttonBox.rejected.connect(ObjectPropertiesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ObjectPropertiesDialog)
        ObjectPropertiesDialog.setTabOrder(self.name, self.simbad)
        ObjectPropertiesDialog.setTabOrder(self.simbad, self.names)
        ObjectPropertiesDialog.setTabOrder(self.names, self.type)
        ObjectPropertiesDialog.setTabOrder(self.type, self.sptype)
        ObjectPropertiesDialog.setTabOrder(self.sptype, self.ra)
        ObjectPropertiesDialog.setTabOrder(self.ra, self.dec)
        ObjectPropertiesDialog.setTabOrder(self.dec, self.date)
        ObjectPropertiesDialog.setTabOrder(self.date, self.observer)
        ObjectPropertiesDialog.setTabOrder(self.observer, self.equipment)
        ObjectPropertiesDialog.setTabOrder(self.equipment, self.position)

    def retranslateUi(self, ObjectPropertiesDialog):
        _translate = QtCore.QCoreApplication.translate
        ObjectPropertiesDialog.setWindowTitle(_translate("ObjectPropertiesDialog", "Object Properties"))
        self.label_6.setText(_translate("ObjectPropertiesDialog", "Date"))
        self.label_4.setText(_translate("ObjectPropertiesDialog", "Spectral type"))
        self.simbad.setText(_translate("ObjectPropertiesDialog", "Find with SIMBAD"))
        self.label_3.setText(_translate("ObjectPropertiesDialog", "Object type"))
        self.label_8.setText(_translate("ObjectPropertiesDialog", "Equipment"))
        self.label_5.setText(_translate("ObjectPropertiesDialog", "Declination"))
        self.label.setText(_translate("ObjectPropertiesDialog", "Object Name"))
        self.label_2.setText(_translate("ObjectPropertiesDialog", "Right Ascension"))
        self.label_7.setText(_translate("ObjectPropertiesDialog", "Observer"))
        self.label_9.setText(_translate("ObjectPropertiesDialog", "Position"))
        self.label_10.setText(_translate("ObjectPropertiesDialog", "Other Names"))

