from algo.algo_node import AlgoNode


class AlgoNodeListener(AlgoNode):

    def __init__(self, id: str, brain, num_cells):
        self.num_cells = num_cells
        super(AlgoNodeListener, self).__init__(id, brain)


    def update(self):
        super(AlgoNodeListener, self).update()
        if self.firing:
            self.firing = False
