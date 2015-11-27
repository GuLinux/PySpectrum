from PyQt5.QtWidgets import QWidget, QVBoxLayout

class QtCommons:
    def nestWidget(parent, child):
        parent.setLayout(QVBoxLayout())
        parent.layout().addWidget(child)
        return child