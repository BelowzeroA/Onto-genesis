from typing import List

from memory.memory_events import MemoryEvent
from memory.working_memory_cell import WorkingMemoryCell, max_charge

memory_limit = 10


class WorkingMemory:

    def __init__(self):
        self.listeners = []
        self.cells: List[WorkingMemoryCell] = []
        for i in range(memory_limit):
            self.cells.append(WorkingMemoryCell())


    def write(self, node):
        for cell in self.cells:
            if cell.free:
                cell.write(node)
                break


    def attach_listener(self, node, event: MemoryEvent):
        self.listeners.append({'node': node, 'event': event})


    def notify_listeners(self, event):
        for listener in self.listeners:
            if listener['event'] == event:
                listener['node'].fire()


    def broadcast(self, num_cells):
        done_cells = 0
        for cell in self.cells:
            if not cell.free:
                cell.node.potential = 2
                cell.node.fire()
                done_cells += 1
            if done_cells == num_cells:
                break


    def check_listeners(self):
        charged = []
        for cell in self.cells:
            if not cell.free and cell.charge == max_charge:
                charged.append(cell)

        if len(charged) == 2:
            self.notify_listeners(MemoryEvent.Two)

        if len(charged) == 1:
            self.notify_listeners(MemoryEvent.One)



    def update(self):
        self.check_listeners()

        for cell in self.cells:
            cell.update()






