# import nltk
from collections import Counter
from tokenizer import Tokenizer
from network import Network
from network2 import Network2
import numpy as np

# nltk.download()
# tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


tokenizer = Tokenizer()
words = []
sentences = []
with open("sample3.txt", 'r', encoding='utf-8') as file:
    lines = file.read().lower()
    sentences = tokenizer.split_into_sentences(lines)
    for line in sentences:
        words += tokenizer.split_into_words(line)

counts = Counter(words)
print(counts)

window_size = 3

word_pair_frequences = {}
for sent in sentences:
    words = tokenizer.split_into_words(sent)
    for word_position in range(len(words)):
        word = words[word_position]

        if word not in word_pair_frequences:
            word_pair_frequences[word] = []

        start_pos = max(0, word_position - window_size)
        end_pos = min(len(words) - 1, word_position + window_size)
        for second_word_position in range(start_pos, end_pos):
            second_word = words[second_word_position]

            if second_word != word:
                word_pair_frequences[word].append(second_word)

for key in word_pair_frequences.keys():
    word_pair_frequences[key] = Counter(word_pair_frequences[key])

vocabulary_len = len(counts.keys())
vocabulary_encoded = {}
number = 0
for key in counts.keys():
    vocabulary_encoded[key] = ++number

vector_length = 3

train_samples = np.zeros((vocabulary_len, vocabulary_len))
column = 0
for row in train_samples:
    row[column] = 1
    column += 1

print(train_samples)

net = Network2((vocabulary_len, vector_length, vocabulary_len))
xor = [
    [[-1.0, -1.0], [0]],
    [[-1.0,  1.0], [1]],
    [[ 1.0, -1.0], [1]],
    [[ 1.0,  1.0], [0]] #If I change her to 1 it converges
]

net.train(xor)

for e in xor:
    net.forward(e[0])
    print (net.activation[2])
"""
train_samples.fill(0)
train_samples[np.arange(vector_length), 1] = 1

# print(word_pair_frequences)
#net = Network([vocabulary_len, 10, vocabulary_len])
net = Network([vocabulary_len, vector_length, vocabulary_len])
#data = [(1, 2), (2, 4), (3, 5), (6, 10), (10, 15)]
data = [([1,0,0], [2,3,4]), ([0,1,0], [2,4,8])]
net.stochastic_gradient_descent(data, 30, 10, 3.0)
"""
