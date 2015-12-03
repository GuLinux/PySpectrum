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
        self.project = Project()
        self.ui.path.textChanged.connect(lambda t: self.project.set_path(t))
        
        
    def __pick_path(self):
        path = QFileDialog.getExistingDirectory(self, 'Pick Project Directory', saved_directory('project_path', [], QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation), self.settings), QFileDialog.ShowDirsOnly)
        save_path(self.settings, 'project_path', (path, 'dir'), lambda f: self.ui.path.setText(f[0]))
        
    def keyPressEvent(self, evt):
      if evt.key() == Qt.Key_Enter or evt.key() == Qt.Key_Return:
        return
        QDialog.keyPressEvent(self.evt)