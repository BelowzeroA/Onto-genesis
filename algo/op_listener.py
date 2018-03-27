from algo.operation import AlgoOperation


class AlgoOperationListener(AlgoOperation):

    def __init__(self, id: str, algorithm, num_cells):
        self.num_cells = num_cells
        super(AlgoOperationListener, self).__init__(id, algorithm)
        self.filter = None
        self.event = None
        self.connected_with = None


    def update(self):
        super(AlgoOperationListener, self).update()
        if self.firing:
            self.firing = False


    def fire_if_conditions(self, wm_context):
        if self.filter:
            if self.filter == 'abstract' and not wm_context['abstract']:
                return
            if self.filter == 'concrete' and not wm_context['concrete']:
                return
        attention_cells = wm_context['attention']
        cells_to_capture = []# attention_cells[0]

        if self.connected_with:
            cell_to_capture = None
            for cell in attention_cells:
                if self._is_cell_connected_with(cell, wm_context):
                    cells_to_capture.append(cell)
                    if len(cells_to_capture) == self.num_cells:
                        break

        for cell in cells_to_capture:
            cell.captured = True
            self.fire()


    def _is_cell_connected_with(self, cell, wm_context):
        if self.connected_with == 'context':
            if not self.algorithm.onto_container.are_nodes_connected(
                    cell.node,
                    wm_context['context'],
                    primary_only=False):
                return False
        elif self.connected_with:
            target_node = self.algorithm.onto_container.get_node_by_pattern(self.connected_with)
            if not self.algorithm.onto_container.are_nodes_connected(
                    cell.node,
                    target_node,
                    primary_only=True):
                return False
        return True
