
class GraphWalker:

    def __init__(self, brain):
        self.brain = brain
        self.resolved = False
        self.current_tick = 0
        self.input_nodes = []


    def resolve(self, input):
        self.input_nodes = self.brain.onto_container.get_nodes_by_pattern(input)
        self.brain.working_memory.context = self.input_nodes[0]
        self.fire_initial()
        self.brain.algo_container.activate_first()
        self.current_tick = 0
        while not self.brain.algo_container.is_finished() and self.current_tick <= 40:
            self.update_state()
            print(self.brain.algo_container.active_algorithm, self.brain.onto_container)
            print(self.brain.working_memory)

        if self.brain.algo_container.finished:
            return self.brain.working_memory.active_cells_content()


    def update_state(self):
        self.current_tick += 1
        self.brain.current_tick = self.current_tick
        algorithm_switched = self.brain.algo_container.update(self.current_tick)
        if self.brain.algo_container.finished:
            return
        elif algorithm_switched:
            self.reset_state()
        self.current_tick += 1
        algorithm_switched = self.brain.algo_container.update(self.current_tick)
        if not self.brain.algo_container.finished:
            if algorithm_switched:
                self.reset_state()
            self.brain.onto_container.update()
            self.brain.working_memory.update()


    def reset_state(self):
        for node in self.brain.onto_container.nodes:
            node.potential = 0
        self.fire_initial()


    def fire_initial(self):
        for node in self.input_nodes:
            node.initial = True
            node.fire()
