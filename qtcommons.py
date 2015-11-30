from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QToolBar, QToolButton, QMenu

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
        
    def addToolbarPopup(toolbar, text, actions = [], popup_mode = QToolButton.InstantPopup):
        button = QToolButton()
        button.setText(text)
        button.setPopupMode(popup_mode)
        button.setMenu(QMenu())
        for action in actions:
            button.menu().addAction(action)
        toolbar.addWidget(button)
        return button