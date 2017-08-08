import numpy as np
import random

class SkipgramNN:

    activation = [] #List of values with the values of activation of each layers
    weightsIn = []
    weightsOut = []

    def __init__(self, vector_size, vocab_size):

        self.vector_size = vector_size
        self.vocab_size = vocab_size
        self.weights_hidden = np.random.uniform(-1, 1, (vector_size, vocab_size))
        self.weights_output = np.random.uniform(-1, 1, (vocab_size, vector_size))

    def forward(self, X):

        #self.sum_hidden = self.sigmoid(self.weights_hidden.dot(X))
        self.sum_hidden = (self.weights_hidden.dot(X))
        #hidden_output_matrix = np.vstack( (self.sum_hidden, np.array([1]) ) )
        self.sum_output = self.weights_output.dot(self.sum_hidden)
        self.output = self.softmax(self.sum_output)
        return self.output

    def backPropagate(self, Y, trainRate = 0.1):

        #Calc of output delta
        error_output = Y - self.output
        # softmax gradient
        delta_output = np.zeros((self.vocab_size, self.vector_size))
        # for each sample in a training set
        for i in range(self.vector_size):
            for j in range(self.vocab_size):
                delta_output[j][i] = self.sum_hidden[i] * error_output[j]

        error_hidden = error_output.T.dot(self.weights_output)
        delta_hidden = np.zeros((self.vector_size, self.vocab_size))
        for i in range(self.vocab_size):
            for j in range(self.vector_size):
                delta_hidden[j][i] = Y[i] * error_hidden[j]

        self.weights_output = self.weights_output + delta_output * trainRate
        self.weights_hidden = self.weights_hidden + delta_hidden * trainRate
        return np.sum((error_output) ** 2) * 0.5

    def sigmoid(self, z, derv = False):
        if derv == False:
            return 1/(1+np.exp(-z))

    def sigmoidPrime(self, z):
        return self.sigmoid(z)*(1-self.sigmoid(z))

    def train(self, samples, trainRate = 0.5, it = 50000):
        for i in range(it):
            error = 0.0
            for sample in samples:
                inputs = np.array(sample[0])
                targets = np.array(sample[1])
                self.forward(inputs)
                error = error + self.backPropagate(targets, trainRate)
            if i % 10 == 0:
                print("epoch ", i, " error = ", error)

    def softmax(self, x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()