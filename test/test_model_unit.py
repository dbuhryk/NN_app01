# coding: utf-8
import unittest
import logging
from app01.app01_model import AppModel

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.model = AppModel()
        self.model.dictionary = dict({
            u'test_string1': u'test_string2',
            u'test_string_u1': u'test_string_u2_®'
        })

    def test_basic_replacement_01(self):
        res = self.model.replace('''
        string_1
        test_string1
        string_2
        ''')
        self.assertTrue('test_string2' in res)

    def test_unicode_01(self):
        res = self.model.replace('''
        string_1
        test_string_u1
        string_2
        ''')
        self.assertTrue('test_string_u2_®' in res)


class DefaultResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.model = AppModel()
        self.model.load_resources()

    def test_replacement_01(self):
        res = self.model.replace('''
        Oracle
        Unicode
        Microsoft
        SAP
        Unicode
        ''')
        self.assertTrue(u'Oracle®' in res)


if __name__ == "__main__":
    unittest.main()
