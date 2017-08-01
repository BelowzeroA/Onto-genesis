import numpy as np

class Neuron:

    weights = []

    def __init__(self, input_size):
        self.input_size = input_size
        self.weights = np.random.randn(input_size)

    def train(self, data, trainRate = 0.1, num_epochs = 2):
        for i in range(num_epochs):
            error = 0.0
            for sample in data:
                inputs = np.array(sample[0])
                target = sample[1]
                y = self.feed_forward(inputs)
                error += pow(y - target, 2)
                delta = trainRate * (y - target) * y * (1 - y) * inputs
                #delta = trainRate * (y - target) * inputs
                self.weights = self.weights - delta

            print("epoch ", i + 1, " error = ", error / len(data))

    def feed_forward(self, input_vector):
        """Return the output of the network if ``a`` is input."""
        return sigmoid(np.dot(self.weights, input_vector))

    def error(self, input_vector, target):
        value = self.feed_forward(input_vector)
        return pow(value - target, 2) / 2

def sigmoid(z):
    """The sigmoid function."""
    return 1.0 / (1.0 + np.exp(-z))
