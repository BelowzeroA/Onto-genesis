from algo.operation import AlgoOperation


class AlgoOperationSignaller(AlgoOperation):

    def __init__(self, id: str, algorithm, num_cells):
        super(AlgoOperationSignaller, self).__init__(id, algorithm)
        self.num_cells = num_cells


    def update(self):
        super(AlgoOperationSignaller, self).update()
        if self.firing:
            self.firing = False
            self.brain.working_memory.broadcast(self.num_cells)

