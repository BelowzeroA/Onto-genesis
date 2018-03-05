from algo.algo_node_types import AlgoNodeType


class AlgoNode:

    def __init__(self, id: str, type: AlgoNodeType):
        self.node_id = id
        self.type = type