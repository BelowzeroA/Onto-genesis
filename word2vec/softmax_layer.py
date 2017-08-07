import numpy as np

class SoftmaxLayer:

    weights = []

    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        self.weights = np.random.randn(output_size, input_size)

    def train(self, data, trainRate = 0.1, num_epochs = 2):
        for i in range(num_epochs):
            error_scalar = 0.0
            for sample in data:
                inputs = np.array(sample[0])
                target = sample[1]
                output = self.feed_forward(inputs)
                error_scalar += self.loss(output, target)
                error = target - output
                gradients = np.zeros((self.output_size, self.input_size))
                for i in range(self.input_size):
                    for j in range(self.output_size):
                        gradients[j][i] = inputs[i] * error[j]

                delta = gradients * trainRate
                self.weights = self.weights + delta

            print("epoch ", i + 1, " error = ", error_scalar)

    def feed_forward(self, input_vector):
        """Return the output of the network if ``a`` is input."""
        y = np.dot(self.weights, input_vector)
        return softmax(y)

    def error(self, input_vector, target):
        value = self.feed_forward(input_vector)
        return (value - target) ** 2 / 2

    def loss(self, output, target):
        return abs(output - target).sum()

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()