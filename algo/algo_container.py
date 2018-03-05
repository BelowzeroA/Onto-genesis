import json

from algo.connection import Connection
from algo.node import Node


class AlgoContainer:
    def __init__(self):
        self.entries = {}
        self.nodes = []
        self.connections = []


    def load(self, filename):
        with open(filename, 'r', encoding='utf-8') as data_file:
            self.entries = json.load(data_file)

        for entry in self.entries['nodes']:
            node = Node(id=entry['id'], pattern=entry['patterns'][0])
            self.nodes.append(node)

        for entry in self.entries['connections']:
            source_node = self.get_node_by_id(entry['source'])
            target_node = self.get_node_by_id(entry['target'])
            connection = Connection(source=source_node, target=target_node)
            self.connections.append(connection)


    def get_node_by_id(self, id):
        nodes = [node for node in self.nodes if node.node_id == id]
        if nodes:
            return nodes[0]
        return None

