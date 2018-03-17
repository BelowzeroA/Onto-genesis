from algo.algo_node import AlgoNode


class AlgoNodeSignaller(AlgoNode):

    def __init__(self, id: str, brain, num_cells):
        super(AlgoNodeSignaller, self).__init__(id, brain)
        self.num_cells = num_cells


    def update(self):
        super(AlgoNodeSignaller, self).update()
        if self.firing:
            self.firing = False
            self.brain.working_memory.broadcast(self.num_cells)

    # def update(self):
    #     active_node = self.brain.working_memory.cells[0]
    #     # if active_node:
    #     #     active_node.fire()
