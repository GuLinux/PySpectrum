#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import *
from pyspectrum_main_window import PySpectrumMainWindow


app = QApplication(sys.argv)
app.setApplicationName('PySpectrum')
w = PySpectrumMainWindow()
w.show()
sys.exit(app.exec_())

