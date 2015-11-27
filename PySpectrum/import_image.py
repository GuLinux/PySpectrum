from ui_import_image import Ui_ImportImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar
from qmathplotwidget import QMathPlotWidget
import matplotlib.pyplot as plt

class ImportImage(QWidget):
    def __init__(self, fits_file):
        super(ImportImage, self).__init__()
        self.fits_file = fits_file
        self.data=fits_file[0].data.astype(float)
        
        self.ui = Ui_ImportImage()
        self.ui.setupUi(self)
        self.ui.image_widget.setLayout(QVBoxLayout())
        self.ui.spatial_plot_widget.setLayout(QVBoxLayout())
        self.ui.spectrum_plot_widget.setLayout(QVBoxLayout())
        
        image_plot = QMathPlotWidget()
        spatial_plot = QMathPlotWidget()
        spectrum_plot = QMathPlotWidget()
        
        self.ui.image_widget.layout().addWidget(image_plot)
        self.ui.spatial_plot_widget.layout().addWidget(spatial_plot)
        self.ui.spectrum_plot_widget.layout().addWidget(spectrum_plot)
        self.image_view = image_plot.axes.imshow(self.data , cmap='gray')
        spatial_plot.axes.plot(self.data.sum(1))
        
        self.toolbar = QToolBar()
        
        self.ui.toolbar_container.setLayout(QVBoxLayout())
        self.ui.toolbar_container.layout().addWidget(self.toolbar)
