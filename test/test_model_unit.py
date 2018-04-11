# coding: utf-8
"""
Test suite for testing Application Model
"""
import unittest
import logging
from app01.app01_model import AppModel

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


class ModelTestCase(unittest.TestCase):
    """
    Tests basic Model functionality with code generated dictionary
    """
    @classmethod
    def setUpClass(cls):
        cls.model = AppModel()
        cls.model.dictionary = dict({
            u'test_string1': u'test_string2',
            u'test_string_u1': u'test_string_u2_®'
        })

    def test_basic_replacement_01(self):
        """
        Tests basic replacement functionality
        """
        res = self.model.replace('''
        string_1
        test_string1
        string_2
        ''')
        self.assertTrue('test_string2' in res)

    def test_unicode_01(self):
        """
        Tests basic UNICODE replacement functionality
        """
        res = self.model.replace('''
        string_1
        test_string_u1
        string_2
        ''')
        self.assertTrue('test_string_u2_®' in res)


class DefaultResourceTestCase(unittest.TestCase):
    """
    Tests basic Model functionality with resource dictionary
    """
    @classmethod
    def setUpClass(cls):
        cls.model = AppModel()
        cls.model.load_resources()

    def test_replacement_01(self):
        """
        Tests basic replacement functionality
        """
        res = self.model.replace('''
        Oracle
        Unicode
        Microsoft
        SAP
        Unicode
        ''')
        self.assertTrue(u'Oracle®' in res)
        self.assertTrue(u'Unicode®' in res)
        self.assertTrue(u'Microsoft®' in res)
        self.assertTrue(u'SAP®' in res)


if __name__ == "__main__":
    unittest.main()
