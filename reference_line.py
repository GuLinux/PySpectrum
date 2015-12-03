import matplotlib
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QLineEdit, QMenu
from pyui.line_edit import Ui_LineEdit
from qtcommons import QtCommons
from moveable_label import MoveableLabel

class GreekLineEdit(QLineEdit):
    def __init__(self, parent = None):
        QLineEdit.__init__(self, parent)
        
    def contextMenuEvent(self, evt):
        menu = self.createStandardContextMenu()
        greek_letters = menu.addAction("Greek Letters")
        greek_letters_menu = QMenu()
        greek_letters.setMenu(greek_letters_menu)
        greek_letters_menu.addAction("α (alpha)", lambda: self.setText(self.text() + " α"))
        greek_letters_menu.addAction("β (beta)", lambda: self.setText(self.text() + " β"))
        greek_letters_menu.addAction("γ (gamma)", lambda: self.setText(self.text() + " γ"))
        greek_letters_menu.addAction("δ (delta)", lambda: self.setText(self.text() + " δ"))
        greek_letters_menu.addAction("ε (epsilon)", lambda: self.setText(self.text() + " ε"))
        greek_letters_menu.addAction("ζ (zeta)", lambda: self.setText(self.text() + " ζ"))
        greek_letters_menu.addAction("η (eta)", lambda: self.setText(self.text() + " η"))
        greek_letters_menu.addAction("θ (theta)", lambda: self.setText(self.text() + " θ"))
        menu.exec(evt.globalPos());


class ReferenceLine:
    def __init__(self, name, wavelength, axes, on_remove, show_wavelength = False, fontsize = 12, position = None, color='#80ff80'):
        self.axes = axes
        self.wavelength = wavelength
        self.name = name
        self.fontsize = fontsize
        self.show_lambda = show_wavelength
        self.on_remove = on_remove
        self.edit_dialog = QDialog()
        self.line = self.axes.axvline(wavelength, color=color)
        self.label = MoveableLabel(axes=axes, on_dblclick = self.edit_dialog.show, x=wavelength + 50, y=0.5, text=name, fontsize=fontsize)
        self.axes.figure.canvas.draw()
        self.press = None
        self.edit_dialog_ui = Ui_LineEdit()
        self.edit_dialog_ui.setupUi(self.edit_dialog)
        self.line_text = QtCommons.nestWidget(self.edit_dialog_ui.line_text_wrapper, GreekLineEdit())
        self.edit_dialog_ui.show_lambda.setChecked(show_wavelength)
        self.edit_dialog_ui.wavelength.setText("{} Å".format(wavelength))
        self.line_text.setText(name)
        self.edit_dialog.accepted.connect(self.update_line)
        self.edit_dialog_ui.reset_default_text.clicked.connect(lambda: self.line_text.setText(name))
        text_size = self.label.get_size()
        self.edit_dialog_ui.text_size.setValue(text_size)
        self.edit_dialog_ui.reset_default_size.clicked.connect(lambda: self.edit_dialog_ui.text_size.setValue(text_size))
        self.edit_dialog_ui.remove_line.clicked.connect(self.edit_dialog.reject)
        self.edit_dialog_ui.remove_line.clicked.connect(self.remove)
        self.update_line()
        if position:
            self.label.set_x(position[0])
            self.label.set_y(position[1])
        
    def update_line(self):
        self.name = self.line_text.text()
        self.show_lambda = self.edit_dialog_ui.show_lambda.isChecked()
        self.fontsize = self.edit_dialog_ui.text_size.value()
        self.label.set_text("{}\n{} Å".format(self.name, self.wavelength) if self.show_lambda else self.name)
        self.label.set_size(self.fontsize)
        self.label.figure.canvas.draw()
        
    def remove(self):
        self.line.remove()
        self.label.remove()
        self.axes.figure.canvas.draw()
        self.on_remove(self)
        