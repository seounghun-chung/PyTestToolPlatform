from PyQt5.QtWidgets import QWidget, QFileSystemModel, QHeaderView, QFileDialog, QMessageBox, QPlainTextEdit, QApplication,QMainWindow
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5 import uic
from config.config import Config

import os

form_class = uic.loadUiType(os.path.join(Config()['PATH']['QtDesignUi'],'main.ui'))[0]

class Main(QMainWindow, form_class):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    m = Main()
    m.show()    
    app.exec_()
