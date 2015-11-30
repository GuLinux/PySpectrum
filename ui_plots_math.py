# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plots_math.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PlotsMath(object):
    def setupUi(self, PlotsMath):
        PlotsMath.setObjectName("PlotsMath")
        PlotsMath.resize(437, 449)
        self.gridLayout = QtWidgets.QGridLayout(PlotsMath)
        self.gridLayout.setObjectName("gridLayout")
        self.plot = QtWidgets.QWidget(PlotsMath)
        self.plot.setObjectName("plot")
        self.gridLayout.addWidget(self.plot, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(PlotsMath)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.spline_degrees = QtWidgets.QSlider(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spline_degrees.sizePolicy().hasHeightForWidth())
        self.spline_degrees.setSizePolicy(sizePolicy)
        self.spline_degrees.setMinimumSize(QtCore.QSize(140, 0))
        self.spline_degrees.setMinimum(2)
        self.spline_degrees.setMaximum(5)
        self.spline_degrees.setProperty("value", 4)
        self.spline_degrees.setOrientation(QtCore.Qt.Horizontal)
        self.spline_degrees.setObjectName("spline_degrees")
        self.gridLayout_2.addWidget(self.spline_degrees, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 334, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.spline_factor = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.spline_factor.setEnabled(True)
        self.spline_factor.setDecimals(3)
        self.spline_factor.setMaximum(1.0)
        self.spline_factor.setSingleStep(0.001)
        self.spline_factor.setProperty("value", 0.0)
        self.spline_factor.setObjectName("spline_factor")
        self.gridLayout_2.addWidget(self.spline_factor, 1, 1, 1, 1)
        self.spline_degrees_value = QtWidgets.QLabel(self.groupBox)
        self.spline_degrees_value.setText("")
        self.spline_degrees_value.setObjectName("spline_degrees_value")
        self.gridLayout_2.addWidget(self.spline_degrees_value, 0, 2, 1, 1)
        self.spline_factor_auto = QtWidgets.QCheckBox(self.groupBox)
        self.spline_factor_auto.setChecked(False)
        self.spline_factor_auto.setObjectName("spline_factor_auto")
        self.gridLayout_2.addWidget(self.spline_factor_auto, 1, 2, 1, 1)
        self.remove_points = QtWidgets.QPushButton(self.groupBox)
        self.remove_points.setObjectName("remove_points")
        self.gridLayout_2.addWidget(self.remove_points, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.retranslateUi(PlotsMath)
        QtCore.QMetaObject.connectSlotsByName(PlotsMath)

    def retranslateUi(self, PlotsMath):
        _translate = QtCore.QCoreApplication.translate
        PlotsMath.setWindowTitle(_translate("PlotsMath", "Form"))
        self.groupBox.setTitle(_translate("PlotsMath", "GroupBox"))
        self.label_2.setText(_translate("PlotsMath", "Spline factor"))
        self.label.setText(_translate("PlotsMath", "Spline degrees"))
        self.spline_factor_auto.setText(_translate("PlotsMath", "Auto"))
        self.remove_points.setText(_translate("PlotsMath", "Remove Points"))

