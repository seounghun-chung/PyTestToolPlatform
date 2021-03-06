from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop
from config.config import Config
from core.console import console

import os
import sys
import logging

logger = logging.getLogger("qt.gui")
form_class = uic.loadUiType(os.path.join(Config()['PATH']['QtDesignUi'],'main.ui'))[0]

class StdoutRedirect(QObject):
    printOccur = pyqtSignal(str, str, name="print")

    def __init__(self, *param):
        QObject.__init__(self, None)
        self.daemon = True
        self.sysstdout = sys.stdout.write
        self.sysstderr = sys.stderr.write

    def stop(self):
        sys.stdout.write = self.sysstdout
        sys.stderr.write = self.sysstderr

    def start(self):
        sys.stdout.write = self.write
        sys.stderr.write = lambda msg : self.write(msg, color="red")

    def write(self, s, color="black"):
        self.printOccur.emit(s, color)

class Main(QMainWindow, form_class):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        # member variable
        self._fmt = QtGui.QTextCharFormat();        
        self._stdout = StdoutRedirect()    
        self._PyQtSignalConnect = console.PyQtSignalConnect()
        
        # view setting            
        self.textBrowser.setFont(QtGui.QFont(self.fontComboBox.currentText(), 9))
        
        # signal connect
        self._stdout.printOccur.connect(lambda x, y: self._append_text(x, y)) # print redirection
        self.fontComboBox.currentFontChanged.connect(lambda x : self.textBrowser.setFont(x))
        self._PyQtSignalConnect.consoleview_clear.connect(lambda : self.clear()) # console.py is connected
        self._PyQtSignalConnect.consoleview_print.connect(lambda x,y : self._append_text('%s\n'%(x),y))
        self.comboBox.keyPressEvent = self._comboBox_keyPressEvent   
        self.dockWidget.visibilityChanged.connect(self._stdout_redirect)

        self.comboBox.setCurrentText("")            
        
    def _comboBox_keyPressEvent(self, e):
        QComboBox.keyPressEvent(self.comboBox, e)
        if e.key() == Qt.Key_Return:
            cmd = self.comboBox.currentText()
            self._append_text('>>> %s\n' % (cmd),color='blue')        
            console.cexec(cmd)
            self.textBrowser.moveCursor(QtGui.QTextCursor.End)            
            self.comboBox.setCurrentText("")
        else:
            pass

    def _stdout_redirect(self, s):
        if s is True:
            self._stdout.start()
        else:
            self._stdout.stop()

    def _append_text(self, msg, color="black"):
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)

        # set user color
        self._fmt.setForeground(QtGui.QBrush(QtGui.QColor(color)));
        self.textBrowser.mergeCurrentCharFormat(self._fmt); 
        self.textBrowser.insertPlainText(msg)
        # refresh textedit show, refer) https://doc.qt.io/qt-5/qeventloop.html#ProcessEventsFlag-enum
        QApplication.processEvents(QEventLoop.AllEvents)
        
    def clear(self):
        self.textBrowser.clear()
        self.comboBox.clear()
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    m = Main()
    m.show()    
    app.exec_()
