# import nltk
from collections import Counter
from tokenizer import Tokenizer
from network2 import Network2
from network3 import Network3
from skipgram_net import SkipgramNet
from neuron import Neuron
from softmax_layer import SoftmaxLayer
from neuron import *
from word2vec import Word2Vec
from model_serializer import ModelSerializer
import numpy as np


w2v = Word2Vec(vector_size=6, window_size=3, minimal_frequency=1)
#w2v.read_text("sample3.txt")
#w2v.train(train_rate=0.5, num_epochs=1000)
serializer = ModelSerializer("models/vectors.pkl")
w2v.load_model(serializer)
similars = w2v.get_similar('cats')
print(similars)
w2v.save_model(serializer)

exit()

net = Network3(5, 8)
net = Network2((8, 5, 8))

# net = SkipgramNN(2, 3)

data = [
    [[1, 0, 0], [0, 0.8, 0.2]],
    [[0, 1, 0], [0.2, 0.1, 0.7]],
    [[0, 0, 1], [0.6, 0.3, 0.1]],
    #[[1, 0, 1], [0.1, 0.9, 0]],
]
data0 = [
    [[1, 0, 0, 0], [0, 0.6, 0.2, 0.2]],
    [[0, 1, 0, 0], [0.2, 0.1, 0.7, 0]],
    [[0, 0, 1, 0], [0.6, 0.3, 0.1, 0]],
    [[0, 0, 0, 1], [0.1, 0.9, 0, 0]],
]

# net = Network2((8, 6, 8))
data = [
    [[1, 0, 0, 0, 0, 0, 0, 0], [0, 0.8, 0, 0.2, 0, 0, 0, 0]],
    [[0, 1, 0, 0, 0, 0, 0, 0], [0, 0.2, 0, 0.1, 0.7, 0, 0, 0]],
    [[0, 0, 1, 0, 0, 0, 0, 0], [0.9, 0, 0, 0, 0, 0, 0.1, 0]],
    [[0, 0, 0, 1, 0, 0, 0, 0], [0.1, 0, 0, 0, 0, 0.9, 0, 0]],
    [[0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0.1, 0.2, 0.7]],
    [[0, 0, 0, 0, 0, 1, 0, 0], [0, 0.1, 0, 0.8, 0, 0.1, 0, 0]],
    [[0, 0, 0, 0, 0, 0, 1, 0], [0, 0.1, 0, 0.3, 0.4, 0.2, 0, 0]],
    [[0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0.8, 0, 0.1, 0, 0, 0.1]]
]

#net.train(data, 0.2, 5000)
out = net.forward(data[0][0])
print(out)
# print(net.weightsIn)

#exit()

net = SkipgramNN(vector_length, 8)

data = [
    [[1, 0, 0, 0, 0, 0, 0, 0], [0, 0.8, 0, 0.2, 0, 0, 0, 0]],
    [[0, 1, 0, 0, 0, 0, 0, 0], [0, 0.2, 0, 0.1, 0.7, 0, 0, 0]],
    [[0, 0, 1, 0, 0, 0, 0, 0], [0.9, 0, 0, 0, 0, 0, 0.1, 0]],
    [[0, 0, 0, 1, 0, 0, 0, 0], [0.1, 0, 0, 0, 0, 0.9, 0, 0]],
    [[0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0.1, 0.2, 0.7]],
    [[0, 0, 0, 0, 0, 1, 0, 0], [0, 0.1, 0, 0.8, 0, 0.1, 0, 0]],
    [[0, 0, 0, 0, 0, 0, 1, 0], [0, 0.1, 0, 0.3, 0.4, 0.2, 0, 0]],
    [[0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0.8, 0, 0.1, 0, 0, 0.1]]
]
output = net.forward([0,1,0,0,0,0,0,0])
net.train(data, 0.3, 100)
"""
net = SkipgramNN(2, 3)

data = [
    [[1, 0, 0], [0.2, 0.8, 0]],
    [[0, 1, 0], [0.9, 0.1, 0]],
    [[0, 0, 1], [0.1, 0.1, .8]],
]

train_samples = np.zeros((3, len(data)))
train_targets = np.zeros((3, len(data)))
for i in range(len(data)):
    t = data[i]
    train_samples[i] = np.array(t[0])
    train_targets[i] = np.array(t[1])

net.train(data, train_samples, train_targets, 0.3, 10)
print(net.weigths_output)
"""
"""sm = SoftmaxLayer(2, 3)

data = [
    [[0.2, 0.8], [0.2, 0.7, 0.1]],
    [[0.1, 0.2], [0.9, 0.1, 0]],
    #[[0.7, 0.2], [0.1, 0.1, .8]],
]
sm.train(data, 1, 20000)
input = data[0][0]
output = sm.feed_forward(input)
#print(output)

neuron = Neuron(3)
data = [0, 1, 1.5]
output = neuron.feed_forward(data)
print(output)
train_data = [
    [[1, 0, 2], 0.3],
    [[0, 1, 1.5], 0.6],
    [[2, 0, 1.5], 0.8]]

#neuron.train(train_data, 0.3, 1000)
output = neuron.feed_forward(data)
print(output)
"""
"""
for e in data:
    net.forward(e[0])
    print (net.activation[2])

train_samples.fill(0)
train_samples[np.arange(vector_length), 1] = 1

# print(word_pair_frequences)
#net = Network([vocabulary_len, 10, vocabulary_len])
net = Network([vocabulary_len, vector_length, vocabulary_len])
#data = [(1, 2), (2, 4), (3, 5), (6, 10), (10, 15)]
data = [([1,0,0], [2,3,4]), ([0,1,0], [2,4,8])]
net.stochastic_gradient_descent(data, 30, 10, 3.0)
"""
