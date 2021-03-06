import numpy as np
import random

class Network2:

    activation = [] #List of values with the values of activation of each layers
    weightsIn = []
    weightsOut = []

    def __init__(self, sizeOfLayers):
        '''
            sizeOfLayers: Tuple with numbers of neurons of each layer
            (in, hidden, out)
        '''
        if len(sizeOfLayers) > 3:
            raise ValueError('Wrong number of layers')

        self.sizeOfLayers = sizeOfLayers
        for i in range(len(sizeOfLayers)):
            #input layer + bias
            self.activation.append(sizeOfLayers[i]*[0.0] + [0.0])

        # Wi = len(Hid) x len(IN)+1(bias)

        #self.weightsIn = np.array([[0.34, 0.45, 0.87, 0.99], [0.1, 0.001, 0.19, 0.65, 0.501], [0.19, 0.65, 0.501]])
        #self.weightsIn = np.array([[0.34, 0.45, 0.87, 0.99], [0.1, 0.001, 0.19, 0.65], [ 0.501, 0.19, 0.65, 0.501]])
        #self.weightsIn = np.array([[0.34, -0.45, 0.87, -0.99], [0.1, 0.001, -0.19, 0.65]])
        self.weightsIn = np.array([[0.34, -0.45, 0.87, 0], [0.1, 0.001, -0.19, 0]])
        self.weightsIn = np.array([[0.34, -0.45, 0.87, 0.3, 0], [0.1, 0.001, -0.19, -0.3, 0]])
        self.weightsIn = np.random.uniform(-1, 1, (sizeOfLayers[1], sizeOfLayers[0] + 1))

        # Wo = len(OUT) x len(Hid)
        #
        self.weightsOut = np.array([[0.34, -0.45, 0], [0.1, 0.19, 0], [0.501, 0.19, 0]])
        self.weightsOut = np.array([[0.34, -0.45, -0.3], [0, 0.1, 0.19], [0.9, 0, 0.501], [0.19, -0.7, 0]])
        self.weightsOut = np.random.uniform(-1, 1, (sizeOfLayers[2], sizeOfLayers[1] + 1))

    def forward(self, X):
        '''
            X: Vetor de entradas
        '''
        #In+bias add ativation vector
        self.activation[0] = np.vstack((np.array([X]).T, np.array([0])))
        #self.activation[0] = np.vstack(np.array([X]).T)
        #sum of (weights x in)
        self.sumHidden = self.weightsIn.dot(self.activation[0])
        #Ativation of hidden layer
        #self.activation[1] =  np.vstack((self.sigmoid(self.sumHidden), np.array([1])))
        self.activation[1] = np.vstack((self.sumHidden, np.array([0])))
        #sum of(out weights x activation of last layer)
        self.sumOut = self.weightsOut.dot(self.activation[1])
        #activation of output
        #self.activation[2] = (self.sigmoid(self.sumOut))
        self.activation[2] = self.softmax(self.sumOut)
        return self.activation[2].T

    def backPropagate(self, Y, trainRate = 0.1):
        '''
            Y: output target
            trainRate:
        '''
        if len(Y) != self.sizeOfLayers[2]:
            raise ValueError('Wrong number of inputs')

        #Calc of output delta
        error_o = Y.T - self.activation[2].T
        out_delta = self.sigmoidPrime(self.activation[2]) * error_o.T
        #out_delta = error_o.T
        #Calc of hidden delta
        error_h = out_delta.T.dot(self.weightsOut)
        #error_h = out_delta.dot(self.weightsOut)
        hidden_delta = self.sigmoidPrime(self.activation[1]) * error_h.T
        #hidden_delta = self.activation[1] * error_h.T

        # update output weights output
        change_o = self.activation[1] * out_delta.T
        for i in range(self.sizeOfLayers[2]):
            for j in range(self.sizeOfLayers[1]):
                self.weightsOut[i][j] = self.weightsOut[i][j] + trainRate*change_o[j][i]
        # update Input weights
        change_h = self.activation[0] * hidden_delta.T
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

    def train(self, target, trainRate = 0.5, it = 1000):
        for i in range(it):
            error = 0.0
            for t in target:
                inputs = np.array(t[0])
                targets = np.array(t[1])
                self.forward(inputs)
                error = error + self.backPropagate(targets, trainRate)
            if i % 1000 == 0:
                print("epoch ", i, " error = ", error)

    def softmax(self, x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()