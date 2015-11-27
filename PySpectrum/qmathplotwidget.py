from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5 import QtWidgets, QtCore
class QMathPlotWidget(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class QImPlotWidget(QMathPlotWidget):
    def __init__(self, imdata, parent=None, **kwargs):
        QMathPlotWidget.__init__(self, parent)
        self.axes_image = self.axes.imshow(imdata, **kwargs)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)