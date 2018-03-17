
class GraphWalker:

    def __init__(self, brain):
        self.brain = brain
        self.resolved = False
        self.current_tick = 0


    def resolve(self, input):
        input_nodes = self.brain.onto_container.get_nodes_by_pattern(input)
        self.fire_initial(input_nodes)
        self.current_tick = 0
        while not self.resolved and self.current_tick < 10:
            self.current_tick += 1
            self.update_state()
            print(self.brain.onto_container)


    def update_state(self):
        for node in self.brain.algo_container.nodes:
            node.update()

        for conn in self.brain.algo_container.connections:
            conn.update()

        for node in self.brain.onto_container.nodes:
            node.update()

        for conn in self.brain.onto_container.connections:
            conn.update()

        self.brain.working_memory.update()


    def fire_initial(self, initial):
        for node in initial:
            node.fire()
