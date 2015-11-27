import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

def get_color(value):
    return plt.cm.jet(value)

app = QApplication(sys.argv)


img = QImage(1000, 100, QImage.Format_ARGB32)

for i in range(0, 1000):
    color = get_color((1000-i)/1000.0)
    qcolor = QColor(color[0]*255, color[1]*255, color[2]*255)  
    for h in range(0, 100):
      img.setPixel(i, h, qcolor.rgba())


label = QLabel()
label.setPixmap(QPixmap.fromImage(img))
label.show()
sys.exit(app.exec())