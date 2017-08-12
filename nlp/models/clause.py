import json


class Clause:
    def __init__(self):
        self.intent = ''
        self.raw_content = {}
        self.tokens = []

    def load(self, filename):
        with open(filename, 'r', encoding='utf-8') as data_file:
            self.raw_content = json.load(data_file)
        self.intent = self.raw_content["intent"]
        self.predicate = self.raw_content["predicate"]
        self.root_node = self.raw_content["tree"][0]
