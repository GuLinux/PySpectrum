# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_plotted_point.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SelectPlottedPoints(object):
    def setupUi(self, SelectPlottedPoints):
        SelectPlottedPoints.setObjectName("SelectPlottedPoints")
        SelectPlottedPoints.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(SelectPlottedPoints)
        self.gridLayout.setObjectName("gridLayout")
        self.smoothing_degree = QtWidgets.QSlider(SelectPlottedPoints)
        self.smoothing_degree.setMinimum(2)
        self.smoothing_degree.setMaximum(5)
        self.smoothing_degree.setOrientation(QtCore.Qt.Horizontal)
        self.smoothing_degree.setObjectName("smoothing_degree")
        self.gridLayout.addWidget(self.smoothing_degree, 1, 2, 1, 1)
        self.smoothing_degree_value = QtWidgets.QLabel(SelectPlottedPoints)
        self.smoothing_degree_value.setObjectName("smoothing_degree_value")
        self.gridLayout.addWidget(self.smoothing_degree_value, 1, 3, 1, 1)
        self.smoothing_factor_auto = QtWidgets.QCheckBox(SelectPlottedPoints)
        self.smoothing_factor_auto.setObjectName("smoothing_factor_auto")
        self.gridLayout.addWidget(self.smoothing_factor_auto, 2, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(SelectPlottedPoints)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(SelectPlottedPoints)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 2, 1, 2)
        self.plot_widget = QtWidgets.QWidget(SelectPlottedPoints)
        self.plot_widget.setObjectName("plot_widget")
        self.gridLayout.addWidget(self.plot_widget, 0, 0, 1, 4)
        self.label = QtWidgets.QLabel(SelectPlottedPoints)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(SelectPlottedPoints)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.x_coordinate = QtWidgets.QSpinBox(SelectPlottedPoints)
        self.x_coordinate.setMaximum(99999999)
        self.x_coordinate.setObjectName("x_coordinate")
        self.gridLayout.addWidget(self.x_coordinate, 3, 2, 1, 2)
        self.smoothing_factor = QtWidgets.QDoubleSpinBox(SelectPlottedPoints)
        self.smoothing_factor.setDecimals(3)
        self.smoothing_factor.setMaximum(1.0)
        self.smoothing_factor.setSingleStep(0.0001)
        self.smoothing_factor.setProperty("value", 0.1)
        self.smoothing_factor.setObjectName("smoothing_factor")
        self.gridLayout.addWidget(self.smoothing_factor, 2, 2, 1, 1)

        self.retranslateUi(SelectPlottedPoints)
        self.buttonBox.accepted.connect(SelectPlottedPoints.accept)
        self.buttonBox.rejected.connect(SelectPlottedPoints.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectPlottedPoints)

    def retranslateUi(self, SelectPlottedPoints):
        _translate = QtCore.QCoreApplication.translate
        SelectPlottedPoints.setWindowTitle(_translate("SelectPlottedPoints", "Select Point"))
        self.smoothing_degree_value.setText(_translate("SelectPlottedPoints", "2"))
        self.smoothing_factor_auto.setText(_translate("SelectPlottedPoints", "Auto"))
        self.label_2.setText(_translate("SelectPlottedPoints", "Smoothing factor"))
        self.label.setText(_translate("SelectPlottedPoints", "Smoothing degree"))
        self.label_3.setText(_translate("SelectPlottedPoints", "Point x coordinate"))

