from core.console.console import usingconsole

@usingconsole
class Example(object):
    def __init__(self, *args, **kwargs):
        self.v = 1
        print('init')
        
    def example1(self):
        print('example1')
        
    def example2(self):
        self.v += 1
        print('example2 : %d' % self.v)
