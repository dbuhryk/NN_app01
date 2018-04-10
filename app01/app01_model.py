import csv
import os


class AppModel:
    def __init__(self):
        self.dictionary = dict()
        self.path = os.path.dirname(__file__)
        self.resources_path = self.path + "/resources/eggs.csv"

    def load_resources(self):
        with open(self.resources_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
            for row in reader:
                self.dictionary.update([row])

    def replace(self, s):
        for key, value in self.dictionary.items():
            s = s.replace(key, value)
        return s
