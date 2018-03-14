from memory.working_memory import WorkingMemory


class Brain:

    def __init__(self, onto_container, algo_container):
        self.onto_container = onto_container
        self.algo_container = algo_container
        self.onto_container.brain = self
        self.algo_container.brain = self
        self.working_memory = WorkingMemory()