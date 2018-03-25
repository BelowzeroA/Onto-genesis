from typing import List

from memory.memory_events import MemoryEvent
from memory.working_memory_cell import WorkingMemoryCell

memory_limit = 10


class WorkingMemory:

    def __init__(self):
        self.listeners = []
        self.context = None
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


    def notify_listeners(self, event, charged_cells, abstract, concrete):
        for listener in self.listeners:
            if listener['event'] == event:
                operation = listener['operation']
                if not operation.algorithm.active:
                    continue
                attention_nodes = [cell.node for cell in charged_cells]
                wm_context = {'context': self.context,
                              'abstract': abstract,
                              'concrete': concrete,
                              'attention': attention_nodes}
                operation.fire_if_conditions(wm_context)


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
        max_potential = 0.0
        for cell in self.cells:
            if not cell.free and cell.charge == WorkingMemoryCell.max_charge:
                if cell.node_potential > max_potential:
                    max_potential = cell.node_potential

        for cell in self.cells:
            if not cell.free and cell.charge == WorkingMemoryCell.max_charge and cell.node_potential == max_potential:
                charged.append(cell)
                abstract &= cell.node.abstract
                concrete &= not cell.node.abstract

        if len(charged) == 2:
            # nodes have different Abstract property
            if not abstract and not concrete:
                self.notify_listeners(MemoryEvent.One, True, False)
                self.notify_listeners(MemoryEvent.One, False, True)
            else:
                # nodes have equal Abstract property
                self.notify_listeners(MemoryEvent.Two, charged, abstract, concrete)

        if len(charged) == 1:
            self.notify_listeners(MemoryEvent.One, charged, abstract, concrete)


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

