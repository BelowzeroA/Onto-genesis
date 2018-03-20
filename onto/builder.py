import re

from onto.node import Node


class OntoBuilder:

    def __init__(self):
        self.nodes = []
        self.connections = []
        self.id_counter = 0


    def load_list_from_file(filename):
        lines = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                lines.append(line.strip())
        return lines


    def build(self, filename):
        lines = OntoBuilder.load_list_from_file(filename)
        for line in lines:
            self._build_graph(line)


    def _find_node_by_pattern(self, pattern):
        nodes = [node for node in self.nodes if node.pattern == pattern]
        if nodes:
            return nodes[0]
        return None


    def _build_graph(self, line):
        matches = re.findall("(\[[\w\d\s]+\])", line)
        make_abstract_node = '+' in line
        make_connection = '*' in line
        for m in matches:
            pattern = m.strip('[').strip(']')
            node = self._find_node_by_pattern(pattern)
            if not node:
                self.id_counter += 1
                node = Node(id=str(self.id_counter), pattern=pattern, container=None, abstract=False)
                self.nodes.append(node)


