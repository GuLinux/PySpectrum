from pyui.project_widget import Ui_ProjectWidget
from project import Project
from PyQt5.QtWidgets import QWidget, QToolBar
from pyspectrum_commons import *
from import_image import ImportImage

class ProjectWidget(QWidget):
    def __init__(self, project, settings):
        QWidget.__init__(self)
        self.ui = Ui_ProjectWidget()
        self.ui.setupUi(self)
        self.project = project
        self.toolbar = QToolBar()
        import_image = lambda: ImportImage.pick(lambda f: self.import_image.emit(f[0]), settings)
        self.toolbar.addAction(ImportImage.icon(), ImportImage.ACTION_TEXT, import_image)
        self.ui.import_image.clicked.connect(import_image)
        self.__refresh()
        
    def __refresh(self):
        self.ui.name.setText(self.project.get_name())
        self.ui.observer.setText(self.project.get_observer())
        self.ui.position.setText(self.project.get_position())
        self.ui.equipment.setText(self.project.get_equipment())
        self.ui.date.setText(self.project.get_date().toString())
        
