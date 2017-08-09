from skipgram_net import *
from collections import Counter
from tokenizer import Tokenizer
import numpy as np


class Word2Vec:

    def __init__(self, vector_size, window_size):
        self.vector_size = vector_size
        self.vocab_size = 0
        self.window_size = window_size

    def read_text(self, filename):
        tokenizer = Tokenizer()
        words = []
        sentences = []
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.read().lower()
            sentences = tokenizer.split_into_sentences(lines)
            for line in sentences:
                words += tokenizer.split_into_words(line)

        counts = Counter(words)
        print(counts)

        word_pair_frequencies = {}
        for sent in sentences:
            words = tokenizer.split_into_words(sent)
            for word_position in range(len(words)):
                word = words[word_position]

                if word not in word_pair_frequencies:
                    word_pair_frequencies[word] = []

                start_pos = max(0, word_position - self.window_size)
                end_pos = min(len(words) - 1, word_position + self.window_size)
                for second_word_position in range(start_pos, end_pos):
                    second_word = words[second_word_position]

                    if second_word != word:
                        word_pair_frequencies[word].append(second_word)

        for key in word_pair_frequencies.keys():
            word_pair_frequencies[key] = Counter(word_pair_frequencies[key])

        self.vocab_size = len(counts.keys())
        vocabulary_encoded = {}
        vocabulary = []
        number = 0
        for key in counts.keys():
            vocabulary_encoded[key] = number
            vocabulary.append(key)
            number += 1

        self.target_probabilities = []
        for i in range(self.vocab_size):
            word = vocabulary[i]
            frequencies = word_pair_frequencies[word]
            probabilities = []
            for j in range(self.vocab_size):
                target_word = vocabulary[j]
                frequency = 0
                if target_word in frequencies:
                    frequency = frequencies[target_word]
                probabilities.append(frequency)

            self.target_probabilities.append(self.softmax(probabilities))


    def train(self):

        train_samples = np.zeros((self.vocab_size, self.vocab_size))
        column = 0
        for row in train_samples:
            row[column] = 1
            column += 1

        dataset = []
        for i in range(self.vocab_size):
            sample = []
            sample.append(train_samples[i])
            sample.append(self.target_probabilities[i])
            dataset.append(sample)

        self.skipgram = SkipgramNet((self.vocab_size, self.vector_size, self.vocab_size))
        self.skipgram.train(dataset, 0.2, 1000)

        out = self.skipgram.forward(dataset[0][0])
        print(out)

    def softmax(self, x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()
