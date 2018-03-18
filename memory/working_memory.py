from typing import List

from memory.memory_events import MemoryEvent
from memory.working_memory_cell import WorkingMemoryCell

memory_limit = 10


class WorkingMemory:

    def __init__(self):
        self.listeners = []
        self.cells: List[WorkingMemoryCell] = []
        for i in range(memory_limit):
            self.cells.append(WorkingMemoryCell())


    def write(self, node):
        node_found = [cell.node for cell in self.cells if not cell.free and cell.node == node]
        if node_found:
            return
        for cell in self.cells:
            if cell.free:
                cell.write(node)
                break


    def attach_listener(self, operation):
        self.listeners.append({'operation': operation, 'event': operation.event})


    def notify_listeners(self, event, abstract, concrete):
        for listener in self.listeners:
            if listener['event'] == event:
                operation = listener['operation']
                if not operation.algorithm.active:
                    continue
                if operation.filter:
                    if operation.filter == 'abstract' and not abstract:
                        continue
                    if operation.filter == 'concrete' and not concrete:
                        continue
                operation.fire()


    def broadcast(self, num_cells):
        done_cells = 0
        max_charge = max(self.cells, key=lambda c: c.charge).charge
        cells_to_broadcast = [cell for cell in self.cells if not cell.free and cell.charge == max_charge]
        for cell in cells_to_broadcast:
            cell.node.potential = 3
            cell.node.fire()
            done_cells += 1
            if done_cells == num_cells:
                break


    def active_cells_content(self):
        max_charge = max(self.cells, key=lambda c: c.charge).charge
        return [cell.node for cell in self.cells if not cell.free and cell.charge == max_charge]


    def check_listeners(self):
        charged = []
        abstract = True
        concrete = True
        for cell in self.cells:
            if not cell.free and cell.charge == WorkingMemoryCell.max_charge:
                charged.append(cell)
                abstract &= cell.node.abstract
                concrete &= not cell.node.abstract

        if len(charged) == 2:
            self.notify_listeners(MemoryEvent.Two, abstract, concrete)

        if len(charged) == 1:
            self.notify_listeners(MemoryEvent.One, abstract, concrete)


    def update(self):
        self.check_listeners()

        for cell in self.cells:
            cell.update()


    def __repr__(self):
        repr = ''
        for cell in self.cells:
            if not cell.free:
                repr += '[ {} ] '.format(cell.node.node_id)
        return repr

