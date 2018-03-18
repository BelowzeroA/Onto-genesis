

class OntoBulder:

    def __init__(self):
        pass


    def load_list_from_file(filename):
        lines = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                lines.append(line.strip())
        return lines


    def build(self, filename):
        lines = OntoBulder.load_list_from_file(filename)