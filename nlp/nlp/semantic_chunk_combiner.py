import random
from ranepacommon import Timer

from yargy.tokenizer import Tokenizer
import numpy as np


def is_noun(token):
    return 'NOUN' in token.forms[0].grammemes or 'UNKN' in token.forms[0].grammemes

def is_adjective(token):
    return 'ADJF' in token.forms[0].grammemes

def is_verb(token):
    return 'VERB' in token.forms[0].grammemes

def is_preposition(token):
    return 'PREP' in token.forms[0].grammemes

def is_nominative(token):
    return 'nomn' in token.forms[0].grammemes

def is_genitive(token):
    return 'gent' in token.forms[0].grammemes

def is_punct(token):
    return 'PUNCT' in token.forms[0].grammemes


feature_func_patterns = {
    'is_noun': lambda token: is_noun(token),
    'is_adjective': lambda token: is_adjective(token),
    'is_verb': lambda token: is_verb(token),
    'is_nominative': lambda token: is_nominative(token),
    'is_genitive': lambda token: is_genitive(token),
    'is_punct': lambda token: is_punct(token),
}

class SemanticChunkCombiner:

    def __init__(self):
        self.execution_timer = Timer()

    def preprocess_samples(self, samples):
        processed_samples = []
        tokenizer = Tokenizer()

        for sample in samples:
            tokens = self.preprocess_sample(sample, tokenizer)

            processed_samples.append(tokens)

        return processed_samples


    def preprocess_sample(self, sample, tokenizer):
        truth_probabilities = np.ndarray((2), buffer=np.array([1, 0]))
        other_probabilities = np.ndarray((2), buffer=np.array([0, 1]))
        ground_truth = False
        raw_tokens = tokenizer(sample)
        prev_token = None
        for token in raw_tokens:
            if not prev_token:
                prev_token = token
                continue

            if is_preposition(prev_token) or is_preposition(token):
                prev_token = token
                continue

            if token.value == '[':
                ground_truth = True
                continue

            if token.value == ']':
                ground_truth = False
                continue

            probabilities = truth_probabilities if ground_truth else other_probabilities
            feature_vector = self.compute_features(prev_token, token)
            dataset.append((feature_vector, probabilities))
            prev_token = token


    def train(self, samples, number_of_epochs=10, rand_seed=3, verbose=False):
        self.execution_timer.start()
        processed_samples = self.preprocess_samples(samples)
        if verbose:
            self.execution_timer.show('preprocessing')

        self.execution_timer.start()
        self.fit(processed_samples, number_of_epochs=number_of_epochs, verbose=verbose)
        if verbose:
            print('')
            self.execution_timer.show('fitting')