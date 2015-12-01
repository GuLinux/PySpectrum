import matplotlib
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox
from ui_line_edit import Ui_LineEdit

# code adapted from here: http://matplotlib.org/users/event_handling.html
class ReferenceLine:
    lock = None

    def __init__(self, name, wavelength, axes, on_remove):
        self.axes = axes
        self.wavelength = wavelength
        self.name = name
        self.on_remove = on_remove
        self.line = self.axes.axvline(wavelength, color='red')
        self.label = axes.text(wavelength + 50, 0.5, name, fontsize=18)
        self.connections = [
            axes.figure.canvas.mpl_connect('button_press_event', self.onclick),
            axes.figure.canvas.mpl_connect('button_release_event', self.onrelease),
            axes.figure.canvas.mpl_connect('motion_notify_event', self.onmove),
            ]
        self.axes.figure.canvas.draw()
        self.press = None
        self.edit_dialog = QDialog()
        self.edit_dialog_ui = Ui_LineEdit()
        self.edit_dialog_ui.setupUi(self.edit_dialog)
        self.edit_dialog_ui.line_text.setText(name)
        self.edit_dialog.accepted.connect(self.update_line)
        self.edit_dialog_ui.reset_default_text.clicked.connect(lambda: self.edit_dialog_ui.line_text.setText(name))
        text_size = self.label.get_size()
        self.edit_dialog_ui.text_size.setValue(text_size)
        self.edit_dialog_ui.reset_default_size.clicked.connect(lambda: self.edit_dialog_ui.text_size.setValue(text_size))
        self.edit_dialog_ui.remove_line.clicked.connect(self.edit_dialog.reject)
        self.edit_dialog_ui.remove_line.clicked.connect(self.remove)
        
    def update_line(self):
        text = self.edit_dialog_ui.line_text.text()
        if(self.edit_dialog_ui.show_lambda.isChecked()):
               text += "\n{}".format(self.wavelength)
        self.label.set_text(text)
        self.label.set_size(self.edit_dialog_ui.text_size.value())
        self.label.figure.canvas.draw()
        
    def remove(self):
        for connection in self.connections:
            self.axes.figure.canvas.mpl_disconnect(connection)
        self.line.remove()
        self.label.remove()
        self.axes.figure.canvas.draw()
        self.on_remove(self)
        
    def onclick(self, event):
        if not self.label.contains(event)[0]: return
        if ReferenceLine.lock is not None: return
        if event.dblclick:
            self.edit_dialog.show()
            return
        ReferenceLine.lock = self
        x0, y0 = self.label.get_unitless_position()
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
        if event.inaxes != self.label.axes: return
        if ReferenceLine.lock is not self: return
        if not self.press: return
    
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
        if ReferenceLine.lock is not self: return
        self.press = None
        ReferenceLine.lock = None

        # turn off the rect animation property and reset the background
        self.label.set_animated(False)
        self.background = None

        # redraw the full figure
        self.label.figure.canvas.draw()
        