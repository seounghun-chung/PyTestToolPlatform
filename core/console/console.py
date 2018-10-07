"""
    console.py is used to connect GUI and FEATURE
    It provides API for controlling GUI / FEATURE
    It can used class object through from features.alloc import *
"""

from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop, QTimer   
from config.config import singleton

import os
import traceback
import sys
import inspect

classObj = list()
def usingconsole(class_):
  '''
  - decorator for using it in console
  - this case is used as singleton pattern 
  '''
  class class_w(class_):
    _instance = None
    def __new__(class_, *args, **kwargs):
      if class_w._instance is None:
          class_w._instance = super(class_w, 
                                    class_).__new__(class_, 
                                                    *args, 
                                                    **kwargs)
          class_w._instance._sealed = False
      return class_w._instance
    def __init__(self, *args, **kwargs):
      if self._sealed:
        return
      super(class_w, self).__init__(*args, **kwargs)
      self._sealed = True
      ''' register class object as global variable. name of var is lower case'''
      globals()[class_w.__name__.lower()] = self
      classObj.append(class_w.__name__.lower())
      
  class_w.__name__ = class_.__name__  
  return class_w

@singleton
class PyQtSignalConnect(QObject):
    consoleview_clear = pyqtSignal()
    script_run = pyqtSignal()
    exampleview = pyqtSignal(str)
    consoleview_print = pyqtSignal(str, str)
    
    def __init__(self, *param):
        QObject.__init__(self, None)

def cexec(arg1, isfile = False):
    """ it is used in consoleview """
    try:
        if isfile is False:
            c = compile(arg1, "<string>", "single")
        else:
            c = arg1
        exec(c, globals())
    except:  # (OverflowError, ValueError, SyntaxError, NameError):
        info = sys.exc_info()
        backtrace = traceback.format_exception(*info)
        for line in backtrace:
            sys.stderr.write(line)
    
def clear():
    """ clear console view """
    _PyQtSignalConnect = PyQtSignalConnect()
    _PyQtSignalConnect.consoleview_clear.emit()
    
def run():
    """ run script """
    _PyQtSignalConnect = PyQtSignalConnect()
    _PyQtSignalConnect.script_run.emit()

def msleep(t):
    ''' sleep t ms '''
    loop = QEventLoop()
    QTimer.singleShot(t, loop.quit)
    loop.exec_()
    
obj = None
def help(obj = None):
    ''' print support functions '''  
    cexec.__doc__ = "private"
    help.__doc__ = "private"
    usingconsole.__doc__ = 'private'
    
    _print = PyQtSignalConnect().consoleview_print.emit
    
    if obj is None:
        func = inspect.getmembers(sys.modules[__name__],
                                  predicate=lambda f: inspect.isfunction(f) and f.__module__ == __name__)
        _print("General Command List", 'darkred')
        func = sorted(func, key = lambda x : x[1].__doc__.lower()
                                    if type(x[1].__doc__) is not type(None) \
                                    else "z")    
        for ii in func:
            if (ii[1].__doc__ != "private"):
                out = "  %s%s : %s" %(ii[0], inspect.formatargspec(*inspect.getfullargspec(ii[1])), ii[1].__doc__)
                _print(out, 'darkblue')

        for ii in classObj:
            _print("%s : object , for getting more information help(%s)" % (ii, ii), 'darkred')
    else:
        func = inspect.getmembers(obj, predicate = inspect.ismethod)  
        if len(func) == 0:
            try:
                inspect.getfullargspec(obj) # pass not support help()
                out = "parameter %s : %s" % (inspect.formatargspec(*inspect.getfullargspec(obj)), obj.__doc__)    
                _print(out, 'darkblue')
            except:
                _print("Not support help()", 'darkblue')
                pass
        else:
            _print("%s Class Method" % obj.__class__.__name__.lower(), 'darkred')
            for ii in func:
                if ii[0] == "__init__":
                    continue
                out = "  %s.%s%s : %s" % (obj.__class__.__name__.lower(), ii[0], inspect.formatargspec(*inspect.getfullargspec(ii[1]))
                                    , ii[1].__doc__)
                _print(out, 'darkblue')
        