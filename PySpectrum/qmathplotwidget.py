from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, QtCore
class QMathPlotWidgetBase(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = self.__init_axes__(fig)
        self.axes.hold(False)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class QMathPlotWidget(QMathPlotWidgetBase):
    def __init__(self, **kwargs):
        QMathPlotWidgetBase.__init__(self, **kwargs)

    def __init_axes__(self, figure):
        return figure.add_subplot(111)

class QImPlotWidget(QMathPlotWidgetBase):
    def __init__(self, imdata, parent=None, **kwargs):
        QMathPlotWidgetBase.__init__(self, parent)
        self.axes_image = self.axes.imshow(imdata, **kwargs)
        self.axes.set_axis_off()
        self.figure.frameon = False

    def __init_axes__(self, figure):
        return figure.add_axes((0,0, 1,1))