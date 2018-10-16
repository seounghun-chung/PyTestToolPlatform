from PyQt5.QtWidgets import QWidget, QFileSystemModel, QHeaderView, QFileDialog, QMessageBox, QPlainTextEdit, QApplication, QListView
from PyQt5.QtGui import QPalette, QColor, QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtCore import QSize, Qt
from PyQt5 import uic
from config.config import Config
from libs.HtmlTestRunner.runner import HTMLTestRunner
from core.example.example import Example

import sys
import os
import unittest
import threading

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
        
        # member variable
        self.__rollbackImporter = RollbackImporter()
        self.__unittest_thread = threading.Thread()
        
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
        self.btnDel.clicked.connect(self._btnDel_clicked)
        self.listView.activated.connect(self._btnRun_clicked)
        self.listView.keyPressEvent = self._listViewKeyPressEvent
        
        self.btnRun.clicked.connect(self._btnRun_clicked)
        self.btnStop.clicked.connect(self._btnStop_clicked)
        
        self.test = Example()

    def _listViewKeyPressEvent(self, event):
        if (event.key() == Qt.Key_Delete):
            self._btnDel_clicked()
        else:
            QListView.keyPressEvent(self.listView, event)
            
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

    def _btnRun_clicked(self):
        """ unittest run start """
        self.btnRun.setEnabled(False)
        
        self.__rollbackImporter.rollbackImports() # clearly make sure test modules    
    
        selectedIndex = self.listView.selectedIndexes()
        selectedItems = [self.testmodel.itemFromIndex(ii) for ii in selectedIndex]
        
        suite = unittest.TestSuite()
        for testcase in selectedItems:
            if testcase.data() is not None:
                suite.addTest(testcase.data())
            else:
                """ parents (filename) is not runnable """
                logger.error("bug")

        if suite.countTestCases() != 0:          
            testinfo = {'Note' : 'None'}    
            if (self.checkBox.checkState() == Qt.Unchecked):
                runner = unittest.TextTestRunner(verbosity=2)    
            else:        
                runner = HTMLTestRunner(output=Config().get('PATH','QtTestReportPath'),
                                        combine_reports=True,
                                        report_name=Config().get('REPORT','HTMLReportFileName'), 
                                        report_title=Config().get('REPORT','HTMLReportTitle'),
                                        open_in_browser=Config().getboolean('REPORT','HTMLReportOpenBrowser'),
                                        template_args=testinfo)   

            if self.__unittest_thread.is_alive() is True:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("unittest is running ..")
                msg.setWindowTitle("Error")
                msg.exec_()
            else:
                self.__unittest_thread = threading.Thread(target = runner.run, args = (suite,))
                self.__unittest_thread.daemon = True
                self.__unittest_thread.start()
        else:
            """ there are not selected item """
            print("there are not selected item")
            logger.debug("there are not selected item")
        self.btnRun.setEnabled(True)                
      
    def _btnStop_clicked(self):
        pass
        
    def _btnDel_clicked(self):
        """ delete selected unittest list """
        print("del btn click")
        selectedIndex = self.listView.selectedIndexes()
        deleteRow = list()
        for select in selectedIndex:
            deleteRow.append((select.row(), select.parent()))
        deleteRow.sort(reverse=True)
        for selectRow in deleteRow:
            self.testmodel.removeRow(selectRow[0], selectRow[1])                
                
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
