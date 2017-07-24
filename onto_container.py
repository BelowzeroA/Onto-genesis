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

    def find_node_by_id(self, _id):

        if isinstance(_id, tuple):
            _id = _id[0]
        entries = list(entry for entry in self.entries if (entry["id"] == _id))
        if len(entries):
            return entries[0]
        return None

    @staticmethod
    def sum_input_weigths(descendants, target_id):

        weight = 0
        for value in descendants.values():
            weight += sum(conn["weight"] for conn in value if conn["node_id"] == target_id)
        return weight

    def find_common_targets_of_type(self, source_nodes, _type):

        descendants = {}
        for node in source_nodes:
            node_id = node["id"]
            descendants[node_id] = []  # set()
            # weight = 0
            for conn in node["connections"]:
                target_node = self.find_node_by_id(conn["target"])
                if target_node and target_node["type"] == _type:
                    weight = conn["sign"]
                    descendants[node_id].append({"node_id": target_node["id"], "weight": weight})

        target_sets = []
        for target_list in descendants.values():
            target_sets.append([target["node_id"] for target in target_list])

        if len(target_sets) < 2:
            return []

        intersection = set(target_sets[0]).intersection(*target_sets[1:])
        if not intersection:
            return []
        else:
            # return [self.find_node_by_id(node_id) for node_id in intersection]
            result = []
            for target_id in intersection:
                weight = self.sum_input_weigths(descendants, target_id)
                result.append({ "node": target_id, "weight": weight})
            return result

