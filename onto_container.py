import json


class OntoContainer:
    def __init__(self):
        self.chat_id = ''
        self.entries = {}

    def load(self, filename):
        with open(filename, 'r', encoding='utf-8') as data_file:
            self.entries = json.load(data_file)

    def find_node(self, clause_part):
        #for entry in self.entries:
        value = clause_part
        if not isinstance(clause_part, str):
            value = clause_part["text"]
        entries = (entry for entry in self.entries if ("patterns" in entry and value in entry["patterns"]))
        if len(entries):
            return entries[0]
        return None
            #if clause_part["text"]:

