import configparser
import os

def singleton(class_):
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
  class_w.__name__ = class_.__name__
  return class_w

@singleton  
class Config(configparser.ConfigParser):
    def __init__(self, *kwarg, **kwargs):
        super(__class__,self).__init__(*kwarg, **kwargs)
        self.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.cfg'))        