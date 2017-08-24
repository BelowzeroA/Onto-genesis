

class Keywords:
    def __init__(self, reader):
        self.items = []
        reader.load_list(self.items)