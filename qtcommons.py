from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QToolBar, QToolButton, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QStandardPaths
import os

class QtCommons:
    def nestWidget(parent, child):
        l = QVBoxLayout()
        l.setContentsMargins(0,0,0,0)
        l.setSpacing(0)
        parent.setLayout(l)
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
        
    def __save_directory_setting_wrapper(settings, key_name, file_obj, on_ok):
        settings.setValue(key_name, os.path.dirname(file_obj[0]))
        on_ok(file_obj)
        
    def __get_directory(key_name, other_keys, default_path, settings):
        if settings.contains(key_name):
            return settings.value(key_name, type=str)
        for key in other_keys:
            if settings.contains(key):
                return settings.value(key, type=str)
        return default_path if default_path else QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
            
        
    def save_file_sticky(title, file_types, on_ok, settings, key_name, other_keys=[], default_path=None):
        directory = QtCommons.__get_directory(key_name, other_keys, default_path, settings)
        QtCommons.save_file(title, file_types, lambda f: QtCommons.__save_directory_setting_wrapper(settings, key_name, f, on_ok), directory)
        
    def open_file_sticky(title, file_types, on_ok, settings, key_name, other_keys=[], default_path=None):
        directory = QtCommons.__get_directory(key_name, other_keys, default_path, settings)
        QtCommons.open_file(title, file_types, lambda f: QtCommons.__save_directory_setting_wrapper(settings, key_name, f, on_ok), directory)

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