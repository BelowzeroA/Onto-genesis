from algo.algo_node_types import AlgoNodeType


class AlgoNode:

    def __init__(self, id: str, brain):
        self.node_id = id
        self.threshold = 0.5
        self.brain = brain
        self.potential = 0
        self.firing = False


    def fire(self):
        self.firing = True


    def update(self):
        if self.potential > self.threshold:
            self.fire()
            self.potential = 0

        if self.firing:
            connections = self.brain.algo_container.get_outgoing_connections(self)
            for connection in connections:
                connection.pulsing = True