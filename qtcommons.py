from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog

class QtCommons:
    def nestWidget(parent, child):
        parent.setLayout(QVBoxLayout())
        parent.layout().addWidget(child)
        return child
    
    def open_file(title, file_types, on_ok, dir=''):
        open_file = QFileDialog.getOpenFileName(None, title, dir, file_types)
        if open_file[0]:
            on_ok(open_file)
        
    def save_file(title, file_types, on_ok, dir=''):
        save_file = QFileDialog.getSaveFileName(None, title, dir, file_types)
        if save_file[0]:
            on_ok(save_file)
        