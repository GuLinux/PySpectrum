from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QToolBar, QToolButton, QMenu, QAction, QLabel, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QStandardPaths, QTimer
from pyui.notification import Ui_Notification
import os

class QtCommons:
    def nestWidget(parent, child):
        l = QVBoxLayout()
        l.setContentsMargins(0,0,0,0)
        l.setSpacing(0)
        parent.setLayout(l)
        parent.layout().addWidget(child)
        return child
    
    def open_files(title, file_types, on_ok, dir='', parent=None):
        def setup_dialog(dialog):
            dialog.setFileMode(QFileDialog.ExistingFiles)
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
            dialog.filesSelected.connect(on_ok)
        QtCommons.__open_dialog__(title, file_types, dir, setup_dialog, parent)
        
    def open_file(title, file_types, on_ok, dir='', parent=None):
        def setup_dialog(dialog):
            dialog.setFileMode(QFileDialog.ExistingFile)
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
            dialog.fileSelected.connect(lambda file:on_ok((file,dialog.selectedNameFilter)))
        QtCommons.__open_dialog__(title, file_types, dir, setup_dialog, parent)

    def open_dir(title, on_ok, dir='', parent=None):
        def setup_dialog(dialog):
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setOption(QFileDialog.ShowDirsOnly)
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
            dialog.fileSelected.connect(lambda f: on_ok((f, )))
        QtCommons.__open_dialog__(title, None, dir, setup_dialog, parent)
            

    def save_file(title, file_types, on_ok, dir='', parent=None):
        def setup_dialog(dialog):
            dialog.setFileMode(QFileDialog.AnyFile)
            dialog.setDefaultSuffix('fit')
            dialog.setAcceptMode(QFileDialog.AcceptSave)
            dialog.fileSelected.connect(lambda file:on_ok((file,dialog.selectedNameFilter)))
        QtCommons.__open_dialog__(title, file_types, dir, setup_dialog, parent)
        
    def __open_dialog__(title, file_types, dir, setup_dialog, parent=None):
        dialog = QFileDialog(parent)
        if file_types: dialog.setNameFilter(file_types)
        dialog.setDirectory(dir)
        dialog.setWindowTitle(title)
        setup_dialog(dialog)
        dialog.finished.connect(lambda: dialog.deleteLater())
        dialog.show()
        
    def addToolbarPopup(toolbar, text = None, icon_name = None, icon_file = None, actions = [], popup_mode = QToolButton.InstantPopup, toolbutton_style=Qt.ToolButtonTextBesideIcon):
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
        if icon_file:
            button.defaultAction().setIcon(QIcon(icon_file))
        for action in actions:
            button.menu().addAction(action)
        toolbar.addWidget(button)
        return button
    
    def notification(text, title=None, parent=None, type='info', timeout=None):
                                            # or BypassWindowManagerHint
        popup = QWidget(parent, Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        ui = Ui_Notification()
        ui.setupUi(popup)
        ui.text.setText(text)
        ui.title.setText(title)
        ui.close.clicked.connect(popup.deleteLater)
        ui.widget.setStyleSheet({
            'info': 'background-color: rgba(126, 214, 255, 220);',
            'warning': 'background-color: rgba(255, 212, 94, 220);',
            'error': 'background-color: rgba(255, 45, 45, 220);',
            'success': 'background-color: rgba(150, 255, 186, 220);',
            }[type])
        popup.move(QApplication.desktop().screen().rect().center() - popup.rect().center())
        popup.setAttribute(Qt.WA_TranslucentBackground, True)
        if timeout:
            timer = QTimer(popup)
            timer.timeout.connect(popup.deleteLater)
            timer.start(timeout*1000)
        popup.show()
        return popup