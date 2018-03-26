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
        if self.connected_with:
            if len(attention_cells) > 1:
                return
            if self.connected_with == 'context':
                if not self.algorithm.onto_container.are_nodes_connected(
                        attention_cells[0].node,
                        wm_context['context'],
                        primary_only=False):
                    return
            elif self.connected_with:
                target_node = self.algorithm.onto_container.get_node_by_pattern(self.connected_with)
                if not self.algorithm.onto_container.are_nodes_connected(
                        attention_cells[0].node,
                        target_node,
                        primary_only=True):
                    return

        attention_cells[0].captured = True
        self.fire()
