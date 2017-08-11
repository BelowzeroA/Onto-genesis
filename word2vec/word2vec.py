from skipgram_net import *
from collections import Counter
from tokenizer import Tokenizer
import numpy as np
from numpy.linalg import norm
from collections import defaultdict
import math


class Word2Vec:

    def __init__(self, vector_size, window_size, minimal_frequency = 0):
        self.vector_size = vector_size
        self.vocab_size = 0
        self.window_size = window_size
        self.vectors = []
        self.vocabulary_encoded = {}
        self.vocabulary = []
        self.trash_words = []
        self.low_frequency_words = []
        self.minimal_frequency = minimal_frequency
        self.load_trash_words("../dictionaries/trash_words.txt")

    def load_trash_words(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for word in file.read().lower().split('\n'):
                self.trash_words.append(word)

    def clean_words(self, words):
        return list(filter(
            lambda word:
                (word not in self.trash_words)
                and (word not in self.low_frequency_words)
                and (word != ''),
            words))

    def read_text(self, filename):
        tokenizer = Tokenizer()
        words = []
        sentences = []
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.read().lower()
            for line in lines.split('\n'):
                sentences += tokenizer.split_into_sentences(line)
            for line in sentences:
                candidate_words = tokenizer.split_into_words(line)
                words += self.clean_words(candidate_words)

        counts = Counter(words)
        for key in counts:
            if counts[key] < self.minimal_frequency:
                self.low_frequency_words.append(key)

        for key in self.low_frequency_words:
            del counts[key]
        print(counts)

        word_pair_frequencies = {}
        for sent in sentences:
            words = tokenizer.split_into_words(sent)
            words = self.clean_words(words)
            for word_position in range(len(words)):
                word = words[word_position]

                if word not in word_pair_frequencies:
                    word_pair_frequencies[word] = []

                start_pos = max(0, word_position - self.window_size)
                end_pos = min(len(words) - 1, word_position + self.window_size)
                for second_word_position in range(start_pos, end_pos):
                    second_word = words[second_word_position]
                    distance = abs(second_word_position - word_position)
                    if distance == 0:
                        continue
                    inverse_distance = self.window_size - distance + 1
                    if second_word != word:
                        word_pair_frequencies[word].append((second_word, inverse_distance))

        for key in word_pair_frequencies.keys():
            words = []
            word_distances = word_pair_frequencies[key]
            word_distances_sums = {}
            distances_sum = 0
            for word_distance in word_distances:
                word = word_distance[0]
                distance = word_distance[1]
                if word in word_distances_sums:
                    word_distances_sums[word] =+ distance
                else:
                    word_distances_sums[word] = distance
                words.append(word)
            counter = Counter(words)
            for word in counter:
                counter[word] *= math.sqrt(word_distances_sums[word])
            word_pair_frequencies[key] = counter

        self.vocab_size = len(counts.keys())

        number = 0
        for key in counts.keys():
            self.vocabulary_encoded[key] = number
            self.vocabulary.append(key)
            number += 1

        self.target_probabilities = []
        for i in range(self.vocab_size):
            word = self.vocabulary[i]
            frequencies = word_pair_frequencies[word]
            probabilities = []
            for j in range(self.vocab_size):
                target_word = self.vocabulary[j]
                frequency = 0
                if target_word in frequencies:
                    frequency = frequencies[target_word]
                probabilities.append(frequency)

            self.target_probabilities.append(self.softmax(probabilities))

    def train(self, train_rate=0.5, num_epochs=1000):

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
        self.vectors = self.skipgram.train(dataset, train_rate, num_epochs)

        # out = self.skipgram.forward(dataset[0][0])
        # print(out)

    def get_similar(self, word, count = 5):
        word_index = self.vocabulary_encoded[word]
        target_vector = self.vectors[word_index]
        result = []
        similarities = defaultdict(float)
        for i in range(self.vocab_size):
            if i != word_index:
                candidate_vector = self.vectors[i]
                similarity = self.cosine_similarity(target_vector, candidate_vector)
                similarities[i] = similarity

        for word_index in sorted(similarities, key=similarities.get, reverse=True):
            target_word = self.vocabulary[word_index]
            similarity = similarities[word_index]
            result.append((target_word, similarity))
            if 0 < count == len(result):
                break

        return result

    def cosine_similarity(self, vec1, vec2):
        return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))

    def save_model(self, serializer):
        model = {}
        model["vocabulary"] = self.vocabulary
        model["vocabulary_encoded"] = self.vocabulary_encoded
        model["vectors"] = self.vectors

        serializer.save_model(model)

    def load_model(self, serializer):
        model = serializer.load_model()
        self.vocabulary = model["vocabulary"]
        self.vocabulary_encoded = model["vocabulary_encoded"]
        self.vectors = model["vectors"]
        self.vocab_size = len(self.vocabulary)

    def softmax(self, x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()
