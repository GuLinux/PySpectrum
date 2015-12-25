import matplotlib
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector, RectangleSelector

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal

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
        
    def plot(self, axes = None, *args, **kwargs):
        axes = axes if axes else self.axes
        _plot = axes.plot(*args, **kwargs)
        try:
            self.apply_zoom(axes)
        except AttributeError:
            self.figure.canvas.draw()
        return _plot
        
    def apply_zoom(self, axes):
        axes.axis(self.zoom_rect)
        self.figure.canvas.draw()
        
    def select_zoom(self, axes = None):
        def on_rect_selected(self,a,b, axes):
            self.zoom_rect = [a.xdata, b.xdata, a.ydata, b.ydata]
            self.rm_element('zoom')
            self.apply_zoom(axes)
        axes = axes if axes else self.axes
        self.add_rectangle_selector('zoom', lambda a,b: on_rect_selected(self, a, b, axes), axes)
        
    def reset_zoom(self, x_range, ymin, ymax, axes = None):
        self.zoom_rect = [x_range[0], x_range[-1], ymin, ymax]
        self.apply_zoom(axes if axes else self.axes)
        
    def rm_element(self, name, redraw = True):
        element = self.elements.pop(name, None)
        if element != None:
            try:
                element.remove()
            except ValueError: #TODO: bug in matplotlib maybe?
                pass
            except AttributeError:
                pass
            del element
        if redraw:
            self.figure.canvas.draw()

    def add_element(self, element, name):
        self.rm_element(name, redraw=False)
        self.elements[name] = element
        self.figure.canvas.draw()
        
    def add_line(self, name, point, type='v', **kwargs):
        self.add_element(self.axes.axvline(point, **kwargs) if type == 'v' else self.axes.axhline(point, **kwargs), name)

    def add_span(self, name, min, max, type='v', **kwargs):
        self.add_element(self.axes.axvspan(min,max, **kwargs) if type == 'v' else self.axes.axhspan(min, max, **kwargs), name)

    def add_span_selector(self, name, callback, axes = None, **kwargs):
        axes = axes if axes else self.axes
        self.add_element(SpanSelector(axes, lambda min, max: self.__on_selected(name, callback, min, max), **kwargs), name)
        
    def add_rectangle_selector(self, name, callback, axes = None, **kwargs):
        axes = axes if axes else self.axes
        self.add_element(RectangleSelector(axes, lambda eclick, erelease: self.__on_selected(name, callback, eclick, erelease), **kwargs), name)
        
    def __on_selected(self, name, callback, *args):
        self.elements[name].active = False
        # self.elements[name].set_active(False)
        self.rm_element(name)
        callback(*args)

class QMathPlotWidget(QMathPlotWidgetBase):
    mouse_moved = pyqtSignal(float, float)

    def __init__(self, **kwargs):
        QMathPlotWidgetBase.__init__(self, **kwargs)
        self.figure.canvas.mpl_connect('motion_notify_event', self.__on_mouse_moved)

    def __init_axes__(self, figure):
        return figure.add_subplot(111)

    def __on_mouse_moved(self, m):
        if m.xdata and m.ydata:
            self.mouse_moved.emit(m.xdata, m.ydata)

class QImPlotWidget(QMathPlotWidgetBase):
    def __init__(self, imdata, parent=None, **kwargs):
        QMathPlotWidgetBase.__init__(self, parent)
        self.axes_image = self.axes.imshow(imdata, **kwargs)
        self.axes.set_axis_off()
        self.figure.frameon = False

    def __init_axes__(self, figure):
        return figure.add_axes((0,0, 1,1))
