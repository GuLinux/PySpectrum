from pyui.project_widget import Ui_ProjectWidget
from project import Project
from PyQt5.QtWidgets import QWidget, QToolBar

class ProjectWidget(QWidget):
    def __init__(self, project):
        QWidget.__init__(self)
        self.ui = Ui_ProjectWidget()
        self.ui.setupUi(self)
        self.project = project
        self.toolbar = QToolBar()
        self.__refresh()
        
    def __refresh(self):
        self.ui.name.setText(self.project.get_name())
        self.ui.observer.setText(self.project.get_observer())
        self.ui.position.setText(self.project.get_position())
        self.ui.equipment.setText(self.project.get_equipment())
        self.ui.date.setText(self.project.get_date().toString())
        
