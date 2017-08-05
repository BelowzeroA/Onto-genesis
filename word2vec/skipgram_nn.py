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

        self.sum_hidden = self.weights_hidden.dot(X)
        #hidden_output_matrix = np.vstack( (self.sum_hidden, np.array([1]) ) )
        self.sum_output = self.weights_output.dot(self.sum_hidden)
        self.output = (self.softmax(self.sum_output))
        return self.output.T

    def backPropagate(self, Y, trainRate = 0.1):

        #Calc of output delta
        error_o = Y.T - self.activation[2].T
        out_delta = self.sigmoidPrime(self.activation[2]) * error_o.T
        #Calc of hidden delta
        error_h = out_delta.T.dot(self.weightsOut)
        hiden_delta = self.sigmoidPrime(self.activation[1]) * error_h.T

        # update output weights output
        change_o = self.activation[1] * out_delta.T
        for i in range(self.sizeOfLayers[2]):
            for j in range(self.sizeOfLayers[1]):
                self.weightsOut[i][j] = self.weightsOut[i][j] + trainRate*change_o[j][i]
        # update Input weights
        change_h = self.activation[0] * hiden_delta.T
        for i in range(self.sizeOfLayers[1]):
            for j in range(self.sizeOfLayers[0]):
                self.weightsIn[i][j] = self.weightsIn[i][j] + trainRate*change_h[j][i]

        #Error
        return np.sum((Y.T - self.activation[2].T)**2)*0.5

    def sigmoid(self, z, derv = False):
        if derv == False:
            return 1/(1+np.exp(-z))

    def sigmoidPrime(self, z):
        return self.sigmoid(z)*(1-self.sigmoid(z))

    def train(self, target, trainRate = 0.5, it = 50000):
        for i in range(it):
            error = 0.0
            for t in target:
                inputs = np.array(t[0])
                targets = np.array(t[1])
                self.forward(inputs)
                error = error + self.backPropagate(targets, trainRate)

    def softmax(self, x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()