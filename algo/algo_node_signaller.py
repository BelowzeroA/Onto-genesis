from algo.algo_node import AlgoNode


class AlgoNodeSignaller(AlgoNode):

    def __init__(self, id: str, brain):
        super(AlgoNodeSignaller, self).__init__(id, brain)


    def update(self):
        active_node = self.brain.working_memory.cells[0]
        active_node.fire()
