import pickle

class ModelSerializer:

    def save_model(self, obj, filename):
        with open(filename, 'wb') as f:
            pickle.dump(obj, f, pickle.DEFAULT_PROTOCOL)

    def load_model(self, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)