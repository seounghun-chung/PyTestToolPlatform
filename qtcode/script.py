from PyQt5.QtWidgets import QWidget, QFileSystemModel, QHeaderView, QFileDialog, QMessageBox, QPlainTextEdit, QApplication
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5 import uic
from config.config import Config

import os

form_class = uic.loadUiType(os.path.join(Config()['PATH']['QtDesignUi'],'script.ui'))[0]

class Script(QWidget, form_class):
    def __init__(self, parent=None):
        super(Script, self).__init__(parent)
        self.setupUi(self)
        
        # treeView Size
        self.splitter.setSizes([Config().getint('SIZE','QtScriptFileExplorer'),(self.size().width()) - Config().getint('SIZE','QtScriptFileExplorer')])
        
        # treeView model create
        self.model = QFileSystemModel()
        self.model.setNameFilters(["*.py"])
        
        # treeView setting
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.setRootPath('./'))
        self.treeView.setAnimated(True)
        self.treeView.setSortingEnabled(False)
        [self.treeView.hideColumn(ii) for ii in range(1,5)]
        self.treeView.header().setStretchLastSection(False)
        self.treeView.header().setSectionResizeMode(0,QHeaderView.Stretch)           
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = Script()
    Form.show()
    sys.exit(app.exec_())
