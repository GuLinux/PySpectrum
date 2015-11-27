from ui_import_image import Ui_ImportImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar
from qmathplotwidget import QMathPlotWidget
import matplotlib.pyplot as plt
from qtcommons import QtCommons

class ImportImage(QWidget):
    def __init__(self, fits_file):
        super(ImportImage, self).__init__()
        self.fits_file = fits_file
        self.data=fits_file[0].data.astype(float)
        
        self.ui = Ui_ImportImage()
        self.ui.setupUi(self)
        
        image_plot = QtCommons.nestWidget(self.ui.image_widget, QMathPlotWidget())
        spatial_plot = QtCommons.nestWidget(self.ui.spatial_plot_widget, QMathPlotWidget())
        spectrum_plot = QtCommons.nestWidget(self.ui.spectrum_plot_widget, QMathPlotWidget())
        
        self.image_view = image_plot.axes.imshow(self.data , cmap='gray')
        spatial_plot.axes.plot(self.data.sum(1))
        
        self.toolbar = QToolBar()
        
        self.ui.toolbar_container.setLayout(QVBoxLayout())
        self.ui.toolbar_container.layout().addWidget(self.toolbar)
