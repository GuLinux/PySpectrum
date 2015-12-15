# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/notification.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Notification(object):
    def setupUi(self, Notification):
        Notification.setObjectName("Notification")
        Notification.resize(259, 107)
        self.gridLayout_2 = QtWidgets.QGridLayout(Notification)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(Notification)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.title = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.title.setText("")
        self.title.setObjectName("title")
        self.horizontalLayout.addWidget(self.title)
        self.close = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close.sizePolicy().hasHeightForWidth())
        self.close.setSizePolicy(sizePolicy)
        self.close.setMaximumSize(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.close.setFont(font)
        self.close.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.close.setFlat(True)
        self.close.setObjectName("close")
        self.horizontalLayout.addWidget(self.close)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.text = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text.sizePolicy().hasHeightForWidth())
        self.text.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.text.setFont(font)
        self.text.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.text.setText("")
        self.text.setObjectName("text")
        self.gridLayout.addWidget(self.text, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(Notification)
        QtCore.QMetaObject.connectSlotsByName(Notification)

    def retranslateUi(self, Notification):
        _translate = QtCore.QCoreApplication.translate
        Notification.setWindowTitle(_translate("Notification", "Form"))
        self.close.setText(_translate("Notification", "×"))

