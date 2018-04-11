# coding: utf-8
"""
Application Model implementation
"""
import os


class AppModel:
    """
    Application Model implementation class
    """
    def __init__(self):
        self.dictionary = dict()
        self.path = os.path.dirname(__file__)
        self.resources_path = self.path + "/resources/Keyword.txt"
        self.call_counter = 0

    def load_resources(self):
        """
        Loads default replacement term list and build replacement dictionary
        """
        with open(self.resources_path, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                line = line.rstrip('\n')
                self.dictionary.update({line: line + u'®'})

    def replace(self, s):
        """
        Replaces all accounts of dictionary terms with term's coupled value in the dictionary
        :param s: string with terms for replacement
        :return: processed string
        """
        for key, value in self.dictionary.items():
            s = s.replace(key, value)
        return s

    def inc_call_counter(self):
        """
        Atomic call counter increment method
        """
        self.call_counter += 1
