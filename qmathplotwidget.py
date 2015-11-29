import matplotlib
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector, RectangleSelector

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
        self.elements = {}
        
    def rm_element(self, name, redraw = True):
        element = self.elements.pop(name, None)
        if element != None:
            try:
                element.remove()
                del element
            except ValueError: #TODO: bug in matplotlib maybe?
                pass
            except AttributeError:
                pass
        if redraw:
            self.figure.canvas.draw()
    

    def add_line(self, name, point, type='v', **kwargs):
        self.rm_element(name, redraw=False)
        self.elements[name] = self.axes.axvline(point, **kwargs) if type == 'v' else self.axes.axhline(point, **kwargs)
        self.figure.canvas.draw()

    def add_span(self, name, min, max, type='v', **kwargs):
        self.rm_element(name, redraw=False)
        self.elements[name] = self.axes.axvspan(min,max, **kwargs) if type == 'v' else self.axes.axhspan(min, max, **kwargs)
        self.figure.canvas.draw()

    def add_span_selector(self, name, callback, **kwargs):
        self.elements[name] = SpanSelector(self.axes, callback, **kwargs)
        
    def add_rectangle_selector(self, name, callback, **kwargs):
        self.elements[name] = RectangleSelector(self.axes, callback, **kwargs)

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