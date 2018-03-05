from algo.node import Node


class Connection:

    def __init__(self, source: Node, target: Node):
        self.source = source
        self.target = target