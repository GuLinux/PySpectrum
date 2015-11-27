from ui_import_image import Ui_ImportImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QDialog, QGridLayout, QDoubleSpinBox, QLabel, QDialogButtonBox
from qmathplotwidget import QMathPlotWidget, QImPlotWidget
import matplotlib.pyplot as plt
from qtcommons import QtCommons
import scipy.ndimage.interpolation


class ImportImage(QWidget):
    def __init__(self, fits_file):
        super(ImportImage, self).__init__()
        self.fits_file = fits_file
        self.data=fits_file[0].data.astype(float)
        
        self.ui = Ui_ImportImage()
        self.ui.setupUi(self)
        
        image_plot = QtCommons.nestWidget(self.ui.image_widget, QImPlotWidget(self.data, cmap='gray'))
        self.spatial_plot = QtCommons.nestWidget(self.ui.spatial_plot_widget, QMathPlotWidget())
        self.spectrum_plot = QtCommons.nestWidget(self.ui.spectrum_plot_widget, QMathPlotWidget())
        
        self.image_view = image_plot.axes_image # .axes.imshow(self.data, cmap='gray')
        self.spatial_plot.axes.plot(self.data.sum(1))
        self.spectrum_plot.axes.plot(self.data.sum(0))
        
        self.toolbar = QToolBar()
        self.toolbar.addAction("Rotate", lambda: self.rotate_dialog.show())
        self.__init_rotate_dialog__()
        
    def __init_rotate_dialog__(self):
        self.degrees = 0
        self.rotate_dialog = QDialog()
        self.rotate_dialog.windowTitle = "Rotate Image"
        rotate_layout = QGridLayout()
        self.rotate_dialog.setLayout(rotate_layout)
        rotate_spinbox = QDoubleSpinBox()
        rotate_spinbox.setRange(0, 360)
        rotate_spinbox.setSingleStep(0.1)
        rotate_spinbox.setDecimals(2)
        rotate_layout.addWidget(QLabel("Enter degrees for image rotation"))
        rotate_layout.addWidget(rotate_spinbox)
        bb = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Close)
        bb.button(QDialogButtonBox.Apply).clicked.connect(lambda: self.rotate(rotate_spinbox.value()))
        bb.button(QDialogButtonBox.Close).clicked.connect(lambda: self.rotate_dialog.accept())
        rotate_layout.addWidget(bb)
        
    def rotate(self, degrees):
        self.degrees = degrees
        self.rotated = scipy.ndimage.interpolation.rotate(self.data, self.degrees)
        self.image_view.set_data(self.rotated)
        self.image_view.figure.canvas.draw()
        self.draw_plot(self.spectrum_plot.axes, 0)
        self.draw_plot(self.spatial_plot.axes, 1)
        
        
    def draw_plot(self, axes, direction):
        axes.clear()
        axes.plot(self.calc_data(direction))
        axes.figure.canvas.draw()
        
    def calc_data(self, direction):
        return (self.rotated - 0).sum(direction)
    