from memory.working_memory import WorkingMemory


class Brain:

    def __init__(self, onto_container, algo_container):
        self.onto_container = onto_container
        self.algo_container = algo_container
        self.working_memory = WorkingMemory()

        self.onto_container.attach_to_brain(self)
        self.algo_container.attach_to_brain(self)
        self.current_tick = 0
