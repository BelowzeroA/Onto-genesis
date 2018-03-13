from algo.algo_node_types import AlgoNodeType


class AlgoNode:

    def __init__(self, id: str, type: AlgoNodeType, algo_container, onto_container):
        self.node_id = id
        self.type = type
        self.algo_container = algo_container
        self.onto_container = onto_container

    def update(self):
        pass