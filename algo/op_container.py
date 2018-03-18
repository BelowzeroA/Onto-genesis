import json

from algo.op_connection import OperationConnection
from algo.op_exit import AlgoOperationExit
from algo.op_listener import AlgoOperationListener
from algo.op_signaller import AlgoOperationSignaller
from memory.memory_events import MemoryEvent


class OperationContainer:
    def __init__(self, onto_container, algorithm):
        self.entries = {}
        self.operations = []
        self.connections = []
        self.onto_container = onto_container
        self.algorithm = algorithm
        self.brain = None


    def load(self, filename):
        with open(filename, 'r', encoding='utf-8') as data_file:
            self.entries = json.load(data_file)

        for entry in self.entries['nodes']:
            op = None
            if entry['type'] == 'signaller':
                op = AlgoOperationSignaller(id=entry['id'], algorithm=self.algorithm, num_cells=entry['num_cells'])
            elif entry['type'] == 'listener':
                op = AlgoOperationListener(id=entry['id'], algorithm=self.algorithm, num_cells=entry['num_cells'])
                op.filter = entry['filter'] if 'filter' in entry else None
                if entry['num_cells'] == 1:
                    op.event = MemoryEvent.One
                elif entry['num_cells'] == 2:
                    op.event = MemoryEvent.Two
            elif entry['type'] == 'exit':
                op = AlgoOperationExit(id=entry['id'], algorithm=self.algorithm)
            if op:
                self.operations.append(op)

        for entry in self.entries['connections']:
            source_node = self.get_node_by_id(entry['source'])
            target_node = self.get_node_by_id(entry['target'])
            connection = OperationConnection(source=source_node, target=target_node)
            self.connections.append(connection)


    def get_node_by_id(self, id):
        ops = [op for op in self.operations if op.node_id == id]
        if ops:
            return ops[0]
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

