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
        self.groupBox_2 = QtWidgets.QGroupBox(PlotsMath)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.operands_listview = QtWidgets.QListView(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.operands_listview.sizePolicy().hasHeightForWidth())
        self.operands_listview.setSizePolicy(sizePolicy)
        self.operands_listview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.operands_listview.setObjectName("operands_listview")
        self.gridLayout_3.addWidget(self.operands_listview, 0, 0, 1, 2)
        self.remove_operand = QtWidgets.QPushButton(self.groupBox_2)
        self.remove_operand.setEnabled(False)
        self.remove_operand.setObjectName("remove_operand")
        self.gridLayout_3.addWidget(self.remove_operand, 1, 0, 1, 1)
        self.clear_operands = QtWidgets.QPushButton(self.groupBox_2)
        self.clear_operands.setEnabled(False)
        self.clear_operands.setObjectName("clear_operands")
        self.gridLayout_3.addWidget(self.clear_operands, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 1, 1, 1)
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
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(PlotsMath)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.operation_type = QtWidgets.QComboBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.operation_type.sizePolicy().hasHeightForWidth())
        self.operation_type.setSizePolicy(sizePolicy)
        self.operation_type.setObjectName("operation_type")
        self.operation_type.addItem("")
        self.operation_type.addItem("")
        self.gridLayout_4.addWidget(self.operation_type, 0, 0, 1, 1)
        self.execute = QtWidgets.QPushButton(self.groupBox_3)
        self.execute.setObjectName("execute")
        self.gridLayout_4.addWidget(self.execute, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 334, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        self.plot = QtWidgets.QWidget(PlotsMath)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setObjectName("plot")
        self.gridLayout.addWidget(self.plot, 0, 0, 4, 1)
        self.actionSelectPointsToRemove = QtWidgets.QAction(PlotsMath)
        self.actionSelectPointsToRemove.setObjectName("actionSelectPointsToRemove")
        self.actionZoom = QtWidgets.QAction(PlotsMath)
        self.actionZoom.setObjectName("actionZoom")
        self.actionReset_Zoom = QtWidgets.QAction(PlotsMath)
        self.actionReset_Zoom.setObjectName("actionReset_Zoom")
        self.actionUndo = QtWidgets.QAction(PlotsMath)
        self.actionUndo.setObjectName("actionUndo")

        self.retranslateUi(PlotsMath)
        QtCore.QMetaObject.connectSlotsByName(PlotsMath)

    def retranslateUi(self, PlotsMath):
        _translate = QtCore.QCoreApplication.translate
        PlotsMath.setWindowTitle(_translate("PlotsMath", "Form"))
        self.groupBox_2.setTitle(_translate("PlotsMath", "Operands"))
        self.remove_operand.setText(_translate("PlotsMath", "Remove"))
        self.clear_operands.setText(_translate("PlotsMath", "Clear"))
        self.groupBox.setTitle(_translate("PlotsMath", "Smooth curve"))
        self.label_2.setText(_translate("PlotsMath", "Spline factor"))
        self.label.setText(_translate("PlotsMath", "Spline degrees"))
        self.spline_factor_auto.setText(_translate("PlotsMath", "Auto"))
        self.groupBox_3.setTitle(_translate("PlotsMath", "Operations"))
        self.operation_type.setItemText(0, _translate("PlotsMath", "Division"))
        self.operation_type.setItemText(1, _translate("PlotsMath", "Arithmetic mean"))
        self.execute.setText(_translate("PlotsMath", "Execute"))
        self.actionSelectPointsToRemove.setText(_translate("PlotsMath", "Select points to remove"))
        self.actionSelectPointsToRemove.setShortcut(_translate("PlotsMath", "Ctrl+R"))
        self.actionZoom.setText(_translate("PlotsMath", "Zoom"))
        self.actionZoom.setShortcut(_translate("PlotsMath", "Ctrl++"))
        self.actionReset_Zoom.setText(_translate("PlotsMath", "Reset Zoom"))
        self.actionReset_Zoom.setShortcut(_translate("PlotsMath", "Ctrl+-"))
        self.actionUndo.setText(_translate("PlotsMath", "Undo"))
        self.actionUndo.setShortcut(_translate("PlotsMath", "Ctrl+Z"))

