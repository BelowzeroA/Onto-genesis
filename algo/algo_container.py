import json

from algo.algo_connection import AlgoConnection
from algo.algo_node import AlgoNode
from algo.algo_node_listener import AlgoNodeListener
from algo.algo_node_signaller import AlgoNodeSignaller
from memory.memory_events import MemoryEvent


class AlgoContainer:
    def __init__(self, onto_container):
        self.entries = {}
        self.nodes = []
        self.connections = []
        self.onto_container = onto_container
        self.brain = None


    def load(self, filename):
        with open(filename, 'r', encoding='utf-8') as data_file:
            self.entries = json.load(data_file)

        for entry in self.entries['nodes']:
            node = None
            if entry['type'] == 'signaller':
                node = AlgoNodeSignaller(id=entry['id'], brain=self.brain, num_cells=entry['num_cells'])
            elif entry['type'] == 'listener':
                node = AlgoNodeListener(id=entry['id'], brain=self.brain, num_cells=entry['num_cells'])
                if entry['num_cells'] == 1:
                    event = MemoryEvent.One
                elif entry['num_cells'] == 2:
                    event = MemoryEvent.Two
                self.brain.working_memory.attach_listener(node, event)
            if node:
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


    def get_outgoing_connections(self, node):
        return [conn for conn in self.connections if conn.source == node]


    def get_incoming_connections(self, node):
        return [conn for conn in self.connections if conn.target == node]


    def print_nodes(self):
        repr = ''
        for node in self.nodes:
            firing_symbol = 'F' if node.firing else ' '
            repr += '[{} {}] '.format(firing_symbol, node.node_id)
        return repr

