# coding: utf-8
import os


class AppModel:
    def __init__(self):
        self.dictionary = dict()
        self.path = os.path.dirname(__file__)
        self.resources_path = self.path + "/resources/Keyword.txt"
        self.call_counter = 0

    def load_resources(self):
        with open(self.resources_path, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                line = line.rstrip('\n')
                self.dictionary.update({line: line + u'®'})

    def replace(self, s):
        for key, value in self.dictionary.items():
            s = s.replace(key, value)
        return s

    def inc_call_counter(self):
        self.call_counter += 1
