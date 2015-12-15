from pyui.project_dialog import Ui_ProjectDialog
from PyQt5.QtWidgets import QDialog, QAction, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QStandardPaths
from pyspectrum_commons import *
from project import Project

class ProjectDialog(QDialog):
    def __init__(self, settings, project = None):
        QDialog.__init__(self)
        self.settings = settings
        self.ui = Ui_ProjectDialog()
        self.ui.setupUi(self)
        pick_path_action = QAction(QIcon(':/folder_open_20'), None, self.ui.path)
        pick_path_action.triggered.connect(self.__pick_path)
        self.ui.path.addAction(pick_path_action, QLineEdit.TrailingPosition)
        self.project = project if project else Project()
        self.ui.path.setText(self.project.get_path())
        self.ui.name.setText(self.project.get_name())
        self.ui.observer.setText(self.project.get_observer())
        self.ui.position.setText(self.project.get_position())
        self.ui.equipment.setText(self.project.get_equipment())
        self.ui.date.setDate(self.project.get_date())
        
        self.ui.path.textChanged.connect(self.project.set_path)
        self.ui.name.textChanged.connect(self.project.set_name)
        self.ui.observer.textChanged.connect(self.project.set_observer)
        self.ui.position.textChanged.connect(self.project.set_position)
        self.ui.equipment.textChanged.connect(self.project.set_equipment)
        self.ui.date.dateChanged.connect(self.project.set_date)
        self.accepted.connect(self.project.save)
        
        
    def __pick_path(self):
        path = QFileDialog.getExistingDirectory(self, 'Pick Project Directory', saved_directory(PROJECTS, [], QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation), self.settings), QFileDialog.ShowDirsOnly)
        self.ui.path.setText(path)
        
    def keyPressEvent(self, evt):
      if evt.key() == Qt.Key_Enter or evt.key() == Qt.Key_Return:
        return
        QDialog.keyPressEvent(self.evt)