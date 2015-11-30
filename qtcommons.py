from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QToolBar, QToolButton, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class QtCommons:
    def nestWidget(parent, child):
        parent.setLayout(QVBoxLayout())
        parent.layout().addWidget(child)
        return child
    
    def open_file(title, file_types, on_ok, dir=''):
        def setup_dialog(dialog):
            dialog.setFileMode(QFileDialog.ExistingFiles)
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
            dialog.fileSelected.connect(lambda file:on_ok((file,dialog.selectedNameFilter)))
        QtCommons.__open_dialog__(title, file_types, dir, setup_dialog)

    def save_file(title, file_types, on_ok, dir=''):
        def setup_dialog(dialog):
            dialog.setFileMode(QFileDialog.AnyFile)
            dialog.setDefaultSuffix('fit')
            dialog.setAcceptMode(QFileDialog.AcceptSave)
            dialog.fileSelected.connect(lambda file:on_ok((file,dialog.selectedNameFilter)))
        QtCommons.__open_dialog__(title, file_types, dir, setup_dialog)

    def __open_dialog__(title, file_types, dir, setup_dialog):
        dialog = QFileDialog()
        dialog.setNameFilter(file_types)
        dialog.setDirectory(dir)
        dialog.setWindowTitle(title)
        setup_dialog(dialog)
        dialog.finished.connect(lambda: dialog.deleteLater())
        dialog.show()
        
    def addToolbarPopup(toolbar, text = None, icon_name = None, actions = [], popup_mode = QToolButton.InstantPopup, toolbutton_style=Qt.ToolButtonTextBesideIcon):
        button = QToolButton()
        button.setToolButtonStyle(toolbutton_style)
        button.setDefaultAction(QAction(button))
        if text:
            button.defaultAction().setText(text)
            button.defaultAction().setIconText(text)
        button.setPopupMode(popup_mode)
        button.setMenu(QMenu())
        if icon_name:
            button.defaultAction().setIcon(QIcon.fromTheme(icon_name))
        for action in actions:
            button.menu().addAction(action)
        toolbar.addWidget(button)
        return button