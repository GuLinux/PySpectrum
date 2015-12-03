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
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
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
        self.actionOpen_Image = QtWidgets.QAction(PySpectrumMainWindow)
        self.actionOpen_Image.setObjectName("actionOpen_Image")
        self.actionCalibrate_FITS = QtWidgets.QAction(PySpectrumMainWindow)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.actionCalibrate_FITS.setIcon(icon)
        self.actionCalibrate_FITS.setObjectName("actionCalibrate_FITS")
        self.actionPlots_Math = QtWidgets.QAction(PySpectrumMainWindow)
        self.actionPlots_Math.setObjectName("actionPlots_Math")
        self.actionFinish_Spectrum = QtWidgets.QAction(PySpectrumMainWindow)
        self.actionFinish_Spectrum.setObjectName("actionFinish_Spectrum")

        self.retranslateUi(PySpectrumMainWindow)
        QtCore.QMetaObject.connectSlotsByName(PySpectrumMainWindow)

    def retranslateUi(self, PySpectrumMainWindow):
        _translate = QtCore.QCoreApplication.translate
        PySpectrumMainWindow.setWindowTitle(_translate("PySpectrumMainWindow", "PySpectrum"))
        self.toolBar.setWindowTitle(_translate("PySpectrumMainWindow", "Main Toolbar"))
        self.actionOpen_Image.setText(_translate("PySpectrumMainWindow", "&Open Image"))
        self.actionOpen_Image.setShortcut(_translate("PySpectrumMainWindow", "Ctrl+I"))
        self.actionCalibrate_FITS.setText(_translate("PySpectrumMainWindow", "&Calibrate FITS"))
        self.actionCalibrate_FITS.setShortcut(_translate("PySpectrumMainWindow", "Ctrl+S"))
        self.actionPlots_Math.setText(_translate("PySpectrumMainWindow", "Plots Math"))
        self.actionFinish_Spectrum.setText(_translate("PySpectrumMainWindow", "Finish Spectrum"))

