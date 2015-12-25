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
import resources_rc
from project_dialog import ProjectDialog
from stack_images import StackImages
from homepage import HomePage
from project_widget import ProjectWidget
from project import Project

class PySpectrumMainWindow(QMainWindow):
    def __init__(self):
        Instances.MainWindow = self
        font = QApplication.instance().font()
        rc('font', **{'family':'serif','serif':[font.defaultFamily()]})
        super(PySpectrumMainWindow, self).__init__()
        self.ui = Ui_PySpectrumMainWindow()
        self.database = sqlite3.connect(os.path.join('data', 'pyspectrum.db'))
        self.ui.setupUi(self)
        self.settings = QSettings("GuLinux", "PySpectrum")
        self.homepage = HomePage(self.settings, self.database)
        self.ui.stackedWidget.addWidget(self.homepage)
        self.windows_menu = QtCommons.addToolbarPopup(self.ui.toolBar, 'Windows', icon_file=':/bullet_list_20')
        self.actionClose = self.ui.toolBar.addAction(QIcon(':/close_20'), "Close")
        self.actionClose.setEnabled(False)
        self.actionClose.triggered.connect(self.close_widget)
        
        self.homepage.import_image.connect(self.open_image)
        self.homepage.calibrate.connect(self.calibrate)
        self.homepage.math.connect(self.plots_math)
        self.homepage.finish.connect(self.finish_spectrum)
        self.homepage.new_project.connect(self.__new_project)
        self.homepage.stack_images.connect(self.__stack_images)
        self.homepage.open_project.connect(self.__open_project)

        self.ui.stackedWidget.currentChanged.connect(self.current_changed)
        self.current_widget_toolbar = None
        self.restoreGeometry(self.settings.value('window_geometry', QByteArray()))
        self.widgets = [(self.homepage, "Home")]
        self.current_changed(self.ui.stackedWidget.indexOf(self.homepage))
        def action_checked(actions, action):
            for a in actions:
                a.setChecked(a == action)
        self.windows_menu.menu().triggered.connect(lambda a: action_checked(self.windows_menu.menu().actions(), a))
        self.__rebuild_windows_menu()

    def closeEvent(self, ev):
        self.settings.setValue('window_geometry', self.saveGeometry())
        QMainWindow.closeEvent(self, ev)
        
    def close_widget(self):
        # TODO: close() on widget
        self.widgets = [w for w in self.widgets if w[0] != self.ui.stackedWidget.currentWidget()]
        self.ui.stackedWidget.currentWidget().deleteLater()
        self.__rebuild_windows_menu()
        
    def current_changed(self, index):
        self.setWindowTitle([w[1] for w in self.widgets if w[0] == self.ui.stackedWidget.currentWidget()][0])
        self.actionClose.setEnabled(self.homepage != self.ui.stackedWidget.currentWidget() )
        if self.current_widget_toolbar:
            self.removeToolBar(self.current_widget_toolbar)
        self.current_widget_toolbar = self.ui.stackedWidget.currentWidget().toolbar
        self.insertToolBar(self.ui.toolBar, self.current_widget_toolbar)
        self.current_widget_toolbar.setVisible(True)
        
    def open_image(self, file, project=None):
        fits_file = self.open_fits(file, "open_image")
        self.__add_widget(ImportImage(fits_file, self.settings, project=project), 'Import Image - {}'.format(os.path.basename(file)))
        
    def __stack_images(self, file):
        fits_file = self.open_fits(file, "open_image")
        self.__add_widget(StackImages(fits_file, self.settings), 'Stack Images')
        
    
    def calibrate(self, file, project=None):
        fits_file = self.open_fits(file, 'open_spectrum')
        self.__add_widget(CalibrateSpectrum(fits_file, self.settings, self.database, project=project), 'Calibrate - {}'.format(os.path.basename(file)))

    def plots_math(self, file, project=None):
        pm = PlotsMath(self.settings, self.database, project=project)
        self.__add_widget(pm, 'Math')
        if file:
            pm.open_fits(file)

    def finish_spectrum(self, file, project=None):
        fits_file = self.open_fits(file, 'open_spectrum')
        self.__add_widget(FinishSpectrum(fits_file, self.settings, self.database, project=project), 'Finish - {}'.format(os.path.basename(file)))

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
            action.setCheckable(True)
            action.setChecked(widget == self.ui.stackedWidget.currentWidget())
            action.triggered.connect(trigger)
            
        self.windows_menu.menu().clear()
        for w in self.widgets:
            add_action(self, w[1], w[0])
        
    def __new_project(self):
        dialog = ProjectDialog(self.settings)
        if dialog.exec() == QDialog.Accepted:
            self.__open_project(dialog.project.path)
            
    def __open_project(self, path):
        project = Project(path)
        LastFilesList.instance().add_file(PROJECTS, project.path)
        project_widget = ProjectWidget(project, self.settings)
        project_widget.import_image.connect(lambda file: self.open_image(file, project=project))
        project_widget.calibrate.connect(lambda file: self.calibrate(file, project=project))
        project_widget.math.connect(lambda file: self.plots_math(file, project=project))
        project_widget.finish.connect(lambda file: self.finish_spectrum(file, project=project))
        self.__add_widget(project_widget, project.get_name())
        
    def print_coordinates(self,x, y):
        self.ui.statusbar.showMessage('Point: x={:.2f}, y={:.2f}'.format(x, y))
        
