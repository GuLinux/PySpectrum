from pyui.pyspectrum_main_window import Ui_PySpectrumMainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from import_image import ImportImage
from calibrate_spectrum import CalibrateSpectrum
from finish_spectrum import FinishSpectrum
from PyQt5.QtCore import QSettings, QByteArray
import os
from astropy.io import fits
from qtcommons import QtCommons
from plots_math import PlotsMath
from pyspectrum_commons import *
import sqlite3
from matplotlib import rc
from PyQt5.QtWidgets import QApplication
import resources.resources
from homepage import HomePage

class PySpectrumMainWindow(QMainWindow):
    def __init__(self):
        font = QApplication.instance().font()
        rc('font', **{'family':'serif','serif':[font.defaultFamily()]})
        super(PySpectrumMainWindow, self).__init__()
        self.ui = Ui_PySpectrumMainWindow()
        self.database = sqlite3.connect('data/pyspectrum.db')
        self.ui.setupUi(self)
        self.settings = QSettings("GuLinux", "PySpectrum")
        self.homepage = HomePage()
        self.ui.stackedWidget.addWidget(self.homepage)
        QtCommons.addToolbarPopup(self.ui.toolBar, 'File', actions=[self.ui.actionOpen_Image,self.ui.actionCalibrate_FITS,self.ui.actionPlots_Math,self.ui.actionFinish_Spectrum])
        self.windows_menu = QtCommons.addToolbarPopup(self.ui.toolBar, 'Windows')
        self.actionClose = self.ui.toolBar.addAction(QIcon(':/close_20'), "Close")
        self.ui.actionOpen_Image.setIcon(QIcon(':/image_20'))
        self.ui.actionCalibrate_FITS.setIcon(QIcon(':/plot_20'))
        self.ui.actionPlots_Math.setIcon(QIcon(':/math_20'))
        self.ui.actionFinish_Spectrum.setIcon(QIcon(':/done_20'))
        self.actionClose.setEnabled(False)
        self.actionClose.triggered.connect(self.close_widget)
        self.ui.actionOpen_Image.triggered.connect(lambda: QtCommons.open_file_sticky('Open FITS Image',FITS_IMG_EXTS, self.open_image, self.settings, IMPORT_IMG_DIR ))
        self.ui.actionCalibrate_FITS.triggered.connect(lambda: QtCommons.open_file_sticky('Open raw FITS Spectrum',FITS_EXTS, self.calibrate, self.settings, RAW_PROFILE_DIR, [IMPORT_IMG_DIR] ))
        self.ui.actionPlots_Math.triggered.connect(self.plots_math)
        self.ui.actionFinish_Spectrum.triggered.connect(lambda: QtCommons.open_file_sticky('Open FITS Spectrum',FITS_EXTS, self.finish_spectrum, self.settings, CALIBRATED_PROFILE_DIR, [RAW_PROFILE_DIR,IMPORT_IMG_DIR] ))
        self.ui.stackedWidget.currentChanged.connect(self.current_changed)
        self.current_widget_toolbar = None
        self.restoreGeometry(self.settings.value('window_geometry', QByteArray()))
        self.widgets = [(self.homepage, "Home")]
        
    def closeEvent(self, ev):
        self.settings.setValue('window_geometry', self.saveGeometry())
        QMainWindow.closeEvent(self, ev)
        
    def close_widget(self):
        # TODO: close() on widget
        self.widgets = [w for w in self.widgets if w[0] != self.ui.stackedWidget.currentWidget()]
        self.ui.stackedWidget.currentWidget().deleteLater()
        self.__rebuild_windows_menu()
        
    def current_changed(self, index):
        self.actionClose.setEnabled(self.homepage != self.ui.stackedWidget.currentWidget() )
        if self.current_widget_toolbar:
            self.removeToolBar(self.current_widget_toolbar)
        self.current_widget_toolbar = self.ui.stackedWidget.currentWidget().toolbar
        self.addToolBar(self.current_widget_toolbar)
        
    def open_image(self, file):
        fits_file = self.open_fits(file[0], "open_image")
        self.__add_widget(ImportImage(fits_file, self.settings), 'Import Image - {}'.format(os.path.basename(file[0])))
    
    def calibrate(self, file):
        fits_file = self.open_fits(file[0], 'open_spectrum')
        self.__add_widget(CalibrateSpectrum(fits_file, self.settings, self.database), 'Calibrate - {}'.format(os.path.basename(file[0])))

    def plots_math(self):
        self.__add_widget(PlotsMath(self.settings, self.database), 'Math')

        
    def finish_spectrum(self, file):
        fits_file = self.open_fits(file[0], 'open_spectrum')
        self.__add_widget(FinishSpectrum(fits_file, self.settings, self.database), 'Finish - {}'.format(os.path.basename(file[0])))

    def open_fits(self, filename, type):
        file = os.path.realpath(filename)
        return fits.open(file)

    def __add_widget(self, widget, title):
        self.widgets.append( (widget, title) )
        self.ui.stackedWidget.addWidget(widget)
        self.ui.stackedWidget.setCurrentWidget(widget)
        self.__rebuild_windows_menu()
        
    def __rebuild_windows_menu(self):
        def add_action(self, name, widget):
            trigger = lambda: self.ui.stackedWidget.setCurrentWidget(widget)
            action = self.windows_menu.menu().addAction(name)
            action.triggered.connect(trigger)
            
        self.windows_menu.menu().clear()
        for w in self.widgets:
            add_action(self, w[1], w[0])    
        