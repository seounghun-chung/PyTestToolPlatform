from PyQt5.QtWidgets import QWidget, QFileSystemModel, QHeaderView, QFileDialog, QMessageBox, QPlainTextEdit, QApplication
from PyQt5.QtGui import QPalette, QColor, QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtCore import QSize, Qt
from PyQt5 import uic
from config.config import Config

import sys
import os
import unittest

form_class = uic.loadUiType(os.path.join(Config()['PATH']['QtDesignUi'],'test.ui'))[0]

class RollbackImporter(object):
    """
    This tricky little class is used to make sure that modules under test
    will be reloaded the next time they are imported.
    """
    def __init__(self):
        self.previousModules = sys.modules.copy()

    def rollbackImports(self):
        for modname in sys.modules.copy().keys():
            if not modname in self.previousModules:
                # Force reload when modname next imported
                del(sys.modules[modname])

class Test(QWidget, form_class):
    def __init__(self, parent=None):
        super(Test, self).__init__(parent)
        self.setupUi(self)
        
        # treeView Size
        self.splitter.setSizes([Config().getint('SIZE','QtTestFileExplorer'),(self.size().width()) - Config().getint('SIZE','QtTestFileExplorer')])
        
        # treeView model create
        self.model = QFileSystemModel()
        self.model.setNameFilters(["*.py"])
        self.testmodel = QStandardItemModel()
        
        # treeView setting
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.setRootPath(Config().get('PATH','QtTestFilePath')))
        self.treeView.setAnimated(True)
        self.treeView.setSortingEnabled(False)
        [self.treeView.hideColumn(ii) for ii in range(1,5)]
        self.treeView.header().setStretchLastSection(False)
        self.treeView.header().setSectionResizeMode(0,QHeaderView.Stretch)           
        
        self.listView.setModel(self.testmodel)
        
        # connect
        self.treeView.activated.connect(self._btnAdd_clicked)
        
    def _btnAdd_clicked(self):
        selectedIndex = self.treeView.selectedIndexes()
        selectedItems = [self.model.filePath(ii) for ii in selectedIndex]
        
        testloader = unittest.TestLoader()        
        
        for ii in selectedItems:
            if (ii[-3:] != ".py"):
                """ python script only can be added """
                print("not python item is selected")
                continue

            try:
                suite = testloader.discover(os.path.dirname(ii), pattern = os.path.basename(ii))

                # is unittest script correct except error ?
                ret,out = self.__extract_exceptiontestunit(suite)
                if ret is False:
                    raise ImportError(out)
                else:
                    pass
            except ImportError as e:
                sys.stderr.write("%s"%e)
                return
                
            testunits = list()
            self.__extract_testunit(suite,testunits)
            
            for testname in testunits:
                child = QStandardItem(str(testname))
                child.setData(testname)
                child.setToolTip(testname._testMethodDoc)
                self.testmodel.insertRow(0, child)
                print("%s is added" % (testname))   
                    
    def __extract_testunit(self, testsuite, testunits):
        """ extract unittest from testsuite discover was used"""
        if type(testsuite._tests[0]) == unittest.suite.TestSuite:
            self.__extract_testunit(testsuite._tests[0], testunits)
        else:
            for ii in testsuite._tests:
                testunits.append(ii) 
                
    def __extract_exceptiontestunit(self, testsuite):
        """ extract error from testsuite discover was used"""
        if type(testsuite._tests[0]) == unittest.suite.TestSuite:
            return self.__extract_exceptiontestunit(testsuite._tests[0])
        else:
            for ii in testsuite._tests:
                if (hasattr(ii,"_exception")):
                    return False, ii._exception
                else:
                    return True, ""
                    
                    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = Script()
    Form.show()
    sys.exit(app.exec_())
