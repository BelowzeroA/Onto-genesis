
class GraphWalker:

    def __init__(self, brain):
        self.brain = brain
        self.resolved = False
        self.current_tick = 0


    def resolve(self, input):
        input_nodes = self.brain.onto_container.get_nodes_by_pattern(input)
        self.fire_initial(input_nodes)
        self.brain.algo_container.activate_first()
        self.current_tick = 0
        while not self.brain.algo_container.is_finished() and self.current_tick <= 10:
            self.current_tick += 1
            self.update_state()
            print(self.brain.onto_container)
            print(self.brain.working_memory)

        if self.brain.algo_container.finished:
            return self.brain.working_memory.active_cells_content()


    def update_state(self):
        self.brain.algo_container.update(self.current_tick)
        if not self.brain.algo_container.finished:
            self.brain.onto_container.update()
            self.brain.working_memory.update()


    def fire_initial(self, initial):
        for node in initial:
            node.initial = True
            node.fire()
