
class FileReader:

    def __init__(self, filename):
        self.filename = filename

    def load_list(self, list_obj):
        with open(self.filename, 'rb') as file:
            for line in file:
                line = line.strip()
                list_obj.append(line)