



class WorkingMemoryCell:

    max_charge = 3

    def __init__(self):
        self.node = None
        self.free = True
        self.charge = 0


    def write(self, node):
        self.node = node
        self.free = False
        self.charge = WorkingMemoryCell.max_charge


    def update(self):
        if self.charge > 0:
            self.charge -= 1
        else:
            self.free = True