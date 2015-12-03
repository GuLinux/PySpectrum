from pyui.homepage import Ui_HomePage
from PyQt5.QtWidgets import QApplication
from pyspectrum_commons import *
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from qtcommons import QtCommons
from PyQt5.QtWidgets import QWidget, QToolBar

class HomePage(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_HomePage()
        self.ui.setupUi(self)
        self.toolbar = QToolBar()
        self.ui.welcome_label.setText(self.ui.welcome_label.text().format("{} {}".format(QApplication.instance().applicationName(), QApplication.instance().applicationVersion())))
        
