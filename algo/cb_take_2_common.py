from algo.computing_block import ComputingBlock


class cbTake2Common(ComputingBlock):

    def __init__(self, container):
        self.container = container


    def run(self, input):
        nodes = [conn.target for conn in self.container.connections if conn.source in input]
        return set(nodes)


