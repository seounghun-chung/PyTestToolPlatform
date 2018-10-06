import unittest
class My_Tests(unittest.TestCase):

    def test_one(self):
        self.assertTrue(True)

    def test_two(self):
        # demonstrate that stdout is captured in passing tests
        print("HOLA CARACOLA")
        self.assertTrue(True)

    def test_three(self):
        self.assertTrue(True)

    def test_1(self):
        ''' test_1 test call '''
        # demonstrate that stdout is captured in failing tests
        print("HELLO")
        self.assertTrue(False)

    def test_2(self):
        self.assertTrue(False)

    def test_3(self):
        self.assertTrue(False)

    def test_z_subs_pass(self):
        for i in range(2):
            with self.subTest(i=i):
                print("i = {}".format(i))  # this won't appear for now
                self.assertEqual(i, i)

    def test_print(self):
        for ii in range(0,10):
            print('%d. test' % ii)
