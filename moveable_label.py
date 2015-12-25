import matplotlib
from matplotlib.text import Text

# code adapted from here: http://matplotlib.org/users/event_handling.html
class MoveableLabel(Text):
    lock = None
    
    def __init__(self, axes, on_dblclick, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.axes = axes
        self.axes.add_artist(self)
        self.connections = [
            axes.figure.canvas.mpl_connect('button_press_event', self.onclick),
            axes.figure.canvas.mpl_connect('button_release_event', self.onrelease),
            axes.figure.canvas.mpl_connect('motion_notify_event', self.onmove),
            ]
        self.press = None
        self.on_dblclick = on_dblclick
                
    def position(self):
        #print(self.get_position())
        return self.get_position()
        #return self.get_unitless_position()
    
    
    def onclick(self, event):
        if not self.contains(event)[0]: return
        if MoveableLabel.lock is not None: return
        if event.dblclick:
            self.on_dblclick(self)
            return
        MoveableLabel.lock = self
        x0, y0 = self.position()
        self.press = x0, y0, event.xdata, event.ydata
        canvas = self.axes.figure.canvas
        axes = self.axes
        self.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)
        
    def onmove(self, event):
        if event.inaxes != self.axes: return
        if MoveableLabel.lock is not self: return
        if not self.press: return
    
        x0, y0, xpress, ypress = self.press
        if not event.xdata or not event.ydata or not xpress or not ypress: return
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.set_x(x0+dx)
        self.set_y(y0+dy)

        canvas = self.figure.canvas
        axes = self.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self)

        # blit just the redrawn area
        canvas.blit(axes.bbox)
    
    def onrelease(self, event):
        if MoveableLabel.lock is not self: return
        self.press = None
        MoveableLabel.lock = None

        # turn off the rect animation property and reset the background
        self.set_animated(False)
        self.background = None

        # redraw the full figure
        self.figure.canvas.draw()
        
    def remove(self):
        for connection in self.connections:
            self.axes.figure.canvas.mpl_disconnect(connection)
        Text.remove(self)
        
