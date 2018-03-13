import json

from algo.algo_connection import AlgoConnection
from algo.algo_node import AlgoNode


class AlgoContainer:
    def __init__(self, onto_container):
        self.entries = {}
        self.nodes = []
        self.connections = []
        self.onto_container = onto_container


    def load(self, filename):
        with open(filename, 'r', encoding='utf-8') as data_file:
            self.entries = json.load(data_file)

        for entry in self.entries['nodes']:
            node = AlgoNode(id=entry['id'], type=entry['type'], onto_container=self.onto_container, algo_container=self)
            self.nodes.append(node)

        for entry in self.entries['connections']:
            source_node = self.get_node_by_id(entry['source'])
            target_node = self.get_node_by_id(entry['target'])
            connection = AlgoConnection(source=source_node, target=target_node)
            self.connections.append(connection)


    def get_node_by_id(self, id):
        nodes = [node for node in self.nodes if node.node_id == id]
        if nodes:
            return nodes[0]
        return None

