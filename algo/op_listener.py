from algo.operation import AlgoOperation


class AlgoOperationListener(AlgoOperation):

    def __init__(self, id: str, algorithm, num_cells):
        self.num_cells = num_cells
        super(AlgoOperationListener, self).__init__(id, algorithm)
        self.filter = None
        self.event = None


    def update(self):
        super(AlgoOperationListener, self).update()
        if self.firing:
            self.firing = False
