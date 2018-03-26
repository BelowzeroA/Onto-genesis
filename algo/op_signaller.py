from algo.operation import AlgoOperation


class AlgoOperationSignaller(AlgoOperation):

    def __init__(self, id: str, algorithm, num_cells):
        super(AlgoOperationSignaller, self).__init__(id, algorithm)
        self.num_cells = num_cells
        self.fired = False


    def update(self):
        super(AlgoOperationSignaller, self).update()
        if self.firing:
            self.firing = False
            # if self.algorithm.brain.current_tick - self.last_firing_tick >
            if not self.fired:
                self.algorithm.brain.working_memory.broadcast(self.num_cells)
            self.fired = True
            # self.last_firing_tick = self.algorithm.brain.current_tick

