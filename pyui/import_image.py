# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/import_image.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImportImage(object):
    def setupUi(self, ImportImage):
        ImportImage.setObjectName("ImportImage")
        ImportImage.resize(638, 615)
        self.gridLayout = QtWidgets.QGridLayout(ImportImage)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(ImportImage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(ImportImage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.spectrum_plot_widget = QtWidgets.QWidget(ImportImage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spectrum_plot_widget.sizePolicy().hasHeightForWidth())
        self.spectrum_plot_widget.setSizePolicy(sizePolicy)
        self.spectrum_plot_widget.setObjectName("spectrum_plot_widget")
        self.verticalLayout.addWidget(self.spectrum_plot_widget)
        self.label_3 = QtWidgets.QLabel(ImportImage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.image_widget = QtWidgets.QWidget(ImportImage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_widget.sizePolicy().hasHeightForWidth())
        self.image_widget.setSizePolicy(sizePolicy)
        self.image_widget.setObjectName("image_widget")
        self.verticalLayout.addWidget(self.image_widget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 3, 1)
        self.spatial_plot_widget = QtWidgets.QWidget(ImportImage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spatial_plot_widget.sizePolicy().hasHeightForWidth())
        self.spatial_plot_widget.setSizePolicy(sizePolicy)
        self.spatial_plot_widget.setObjectName("spatial_plot_widget")
        self.gridLayout.addWidget(self.spatial_plot_widget, 1, 0, 1, 2)
        self.delta_label = QtWidgets.QLabel(ImportImage)
        self.delta_label.setText("")
        self.delta_label.setObjectName("delta_label")
        self.gridLayout.addWidget(self.delta_label, 2, 0, 1, 2)

        self.retranslateUi(ImportImage)
        QtCore.QMetaObject.connectSlotsByName(ImportImage)

    def retranslateUi(self, ImportImage):
        _translate = QtCore.QCoreApplication.translate
        ImportImage.setWindowTitle(_translate("ImportImage", "Import Image"))
        self.label.setText(_translate("ImportImage", "Spatial Plot"))
        self.label_2.setText(_translate("ImportImage", "Spectrum"))
        self.label_3.setText(_translate("ImportImage", "Image"))
        self.spatial_plot_widget.setToolTip(_translate("ImportImage", "<html><head/><body><p>Rotate the image until you see a single thin vertical spike</p></body></html>"))

