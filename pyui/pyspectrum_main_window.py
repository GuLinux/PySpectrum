# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/pyspectrum_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PySpectrumMainWindow(object):
    def setupUi(self, PySpectrumMainWindow):
        PySpectrumMainWindow.setObjectName("PySpectrumMainWindow")
        PySpectrumMainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(PySpectrumMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)
        PySpectrumMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(PySpectrumMainWindow)
        self.statusbar.setObjectName("statusbar")
        PySpectrumMainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(PySpectrumMainWindow)
        self.toolBar.setIconSize(QtCore.QSize(16, 16))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar.setObjectName("toolBar")
        PySpectrumMainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(PySpectrumMainWindow)
        self.stackedWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(PySpectrumMainWindow)

    def retranslateUi(self, PySpectrumMainWindow):
        _translate = QtCore.QCoreApplication.translate
        PySpectrumMainWindow.setWindowTitle(_translate("PySpectrumMainWindow", "PySpectrum"))
        self.toolBar.setWindowTitle(_translate("PySpectrumMainWindow", "Main Toolbar"))

