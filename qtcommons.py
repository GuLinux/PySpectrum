from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog

class QtCommons:
    def nestWidget(parent, child):
        parent.setLayout(QVBoxLayout())
        parent.layout().addWidget(child)
        return child
    
    def open_file(title, file_types, on_ok, dir=''):
        dialog = QFileDialog()
        dialog.setNameFilter(file_types)
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setDirectory(dir)
        dialog.setWindowTitle(title)
        dialog.fileSelected.connect(lambda file:on_ok((file,dialog.selectedNameFilter)))
        dialog.finished.connect(lambda: dialog.deleteLater())
        dialog.show()
        
    def save_file(title, file_types, on_ok, dir=''):
        save_file = QFileDialog.getSaveFileName(None, title, dir, file_types)
        if save_file[0]:
            on_ok(save_file)
        
