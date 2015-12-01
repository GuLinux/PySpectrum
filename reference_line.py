import matplotlib

class ReferenceLine:

    def __init__(self, name, wavelength, axes):
        self.axes = axes
        self.wavelength = wavelength
        self.name = name
        self.line = self.axes.axvline(wavelength, color='red')
        self.label = axes.text(wavelength, 0.5, name, fontsize=18)
        axes.figure.canvas.mpl_connect('button_press_event', self.onclick)
        axes.figure.canvas.mpl_connect('button_release_event', self.onrelease)
        axes.figure.canvas.mpl_connect('motion_notify_event', self.onmove)
        self.axes.figure.canvas.draw()
        self.dragging = False
        self.press = None
        self.live = True
        
    def remove(self):
        self.line.remove()
        self.label.remove()
        self.axes.figure.canvas.draw()
        
    def onclick(self, event):
        if not self.live: return
        if not self.__check_bbox(event):
            return
        if event.dblclick:
            self.remove()
            return
        
        x0 = event.xdata
        y0 = event.ydata
        self.press = x0, y0, event.xdata, event.ydata

        canvas = self.axes.figure.canvas
        axes = self.axes
        self.label.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.label)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)
        
    def onmove(self, event):
        if not self.live: return
        if event.inaxes != self.label.axes: return
        if not self.press:
            return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.label.set_x(x0+dx)
        self.label.set_y(y0+dy)

        canvas = self.label.figure.canvas
        axes = self.label.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.label)

        # blit just the redrawn area
        canvas.blit(axes.bbox)        
    def onrelease(self, event):
        if not self.live: return
        self.press = None
        #DraggableRectangle.lock = None

        # turn off the rect animation property and reset the background
        self.label.set_animated(False)
        self.background = None

        # redraw the full figure
        self.label.figure.canvas.draw()
        
        
    def __check_bbox(self, event):
        return self.label.contains(event)[0]