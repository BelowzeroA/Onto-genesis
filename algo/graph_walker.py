from algo.cb_take_1_common import cbTake1Common
from algo.cb_take_2_common import cbTake2Common


class GraphWalker:

    def __init__(self, onto_container, algo_container):
        self.onto_container = onto_container
        self.algo_container = algo_container
        self.resolved = False
        self.current_tick = 0


    def resolve(self, input):
        self.fire_initial(input)
        self.current_tick = 0
        while not self.resolved:
            self.current_tick += 1
            self.update_state()


    def update_state(self):
        for node in self.algo_container.nodes:
            node.update()

        for conn in self.algo_container.connections:
            conn.update()

        for node in self.onto_container.nodes:
            node.update()

        for conn in self.onto_container.connections:
            conn.update()


    def fire_initial(self, initial):
        for node in initial:
            node.fire()
