import ntpath

from algo.op_container import OperationContainer


class Algorithm:

    def __init__(self, onto_container, filename):
        self.algo_id = id
        self.name = ntpath.basename(filename)
        self.container = OperationContainer(onto_container=onto_container, algorithm=self)
        self.container.load(filename)
        self.onto_container = onto_container
        self.active = False
        self.finished = False
        self.time_exceeded = False
        self.start_tick = 0
        self.current_tick = 0
        self.wait_ticks = self.container.entries['waiting']
        self.next = None


    def start(self, tick):
        self.start_tick = tick
        self.current_tick = tick
        self.active = True


    def update(self, tick):

        if self.active:
            self.current_tick = tick
            if self.current_tick - self.start_tick >= self.wait_ticks:
                self.time_exceeded = True
                self.active = False
                return

            for op in self.container.operations:
                op.update()
            for conn in self.container.connections:
                conn.update()

