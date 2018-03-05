from algo.computing_block import ComputingBlock


class cbTake1Common(ComputingBlock):

    def __init__(self, container):
        self.container = container


    def run(self, input):
        all_nodes = set([conn.target for conn in self.container.connections if conn.source in input])
        for input_node in input:
            nodes = set([conn.target for conn in self.container.connections if conn.source == input_node])
            all_nodes &= nodes
        if len(all_nodes) == 1:
            return all_nodes
        return None


