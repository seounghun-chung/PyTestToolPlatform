import unittest
import warnings
class My_Tests(unittest.TestCase):

    def test_one(self):
        self.assertTrue(True)
        warnings.warn('test warning1')
    def test_two(self):
        # demonstrate that stdout is captured in passing tests
        print("HOLA CARACOLA")
        warnings.warn('test warning2')        
        warnings.warn('test warning3')        
        warnings.warn('test warning4')        
        self.assertTrue(True)
    def test_error(self):
        a
    def test_three(self):
        self.assertTrue(True)

    def test_1(self):
        ''' test_1 test call '''
        # demonstrate that stdout is captured in failing tests
        print("HELLO")
        self.assertTrue(False)

    @unittest.skip('pass')
    def test_2(self):
        self.assertTrue(False)

    def test_3(self):
        warnings.warn('test warning5')            
        self.assertTrue(False)

    def test_z_subs_pass(self):
        for i in range(2):
            with self.subTest(i=i):
                print("i = {}".format(i))  # this won't appear for now
                self.assertEqual(i, i)

    def test_print(self):
        for ii in range(0,10):
            print('%d. test' % ii)
