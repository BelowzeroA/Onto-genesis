import pickle

class ModelSerializer:

    def __init__(self, filename):
        self.filename = filename

    def save_model(self, obj):
        with open(self.filename, 'wb') as f:
            pickle.dump(obj, f, pickle.DEFAULT_PROTOCOL)

    def load_model(self):
        with open(self.filename, 'rb') as f:
            return pickle.load(f)