import json


class OntoContainer:
    def __init__(self):
        self.chat_id = ''
        self.entries = {}

    def load(self, filename):
        with open(filename, 'r', encoding='utf-8') as data_file:
            self.entries = json.load(data_file)

    def find_node(self, clause_part):
        # for entry in self.entries:
        value = clause_part
        if not isinstance(clause_part, str):
            value = clause_part["text"]
        entries = list(entry for entry in self.entries if ("patterns" in entry and value in entry["patterns"]))
        if len(entries):
            return entries[0]
        return None

    def find_node_by_id(self, id):

        entries = list(entry for entry in self.entries if (entry["id"] == id))
        if len(entries):
            return entries[0]
        return None

    def find_common_targets_of_type(self, source_nodes, _type):

        descendants = {}
        for node in source_nodes:
            node_id = node["id"]
            descendants[node_id] = set()
            for conn in node["connections"]:
                target_node = self.find_node_by_id(conn["target"])
                if target_node and target_node["type"] == _type:
                    descendants[node_id].add(target_node["id"])

        sets = list(descendants.values())
        intersection = set(sets[0]).intersection(*sets[1:])
        if not intersection:
            return []
        else:
            return [self.find_node_by_id(node_id) for node_id in intersection]