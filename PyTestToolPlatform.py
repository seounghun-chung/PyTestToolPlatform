from PyQt5.QtWidgets import QWidget, QFileSystemModel, QHeaderView, QFileDialog, QMessageBox, QPlainTextEdit, QApplication,QMainWindow
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5 import uic

from qtcode.main import Main

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    m = Main()
    m.show()    
    app.exec_()
