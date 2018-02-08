import random
from ranepacommon import Timer

from yargy.tokenizer import Tokenizer
import numpy as np

from networks.feedforward_network import FeedforwardNetwork


def is_noun(token):
    return 'NOUN' in token.forms[0].grammemes or 'UNKN' in token.forms[0].grammemes

def is_adjective(token):
    return 'ADJF' in token.forms[0].grammemes

def is_verb(token):
    return 'VERB' in token.forms[0].grammemes

def is_infinitive(token):
    return 'INFN' in token.forms[0].grammemes

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
    'is_infinitive': lambda token: is_infinitive(token),
    'is_nominative': lambda token: is_nominative(token),
    'is_genitive': lambda token: is_genitive(token),
    'is_punct': lambda token: is_punct(token),
}


class SemanticChunkCombiner:

    def __init__(self):
        self.execution_timer = Timer()

    def generate_dataset(self, samples):
        dataset = []
        tokenizer = Tokenizer()

        for sample in samples:
            self.populate_dataset_from_sample(sample, dataset, tokenizer)

        return dataset


    def populate_dataset_from_sample(self, sample, dataset, tokenizer):

        ground_truth = False
        raw_tokens = tokenizer(sample)
        prev_token = None
        environment_features = {'punct_between': 0, 'preposition_between': 0, 'preposition_before': 0}
        for token in raw_tokens:

            token.chunked = False
            if token.value == '[':
                ground_truth = True
                continue

            if not prev_token:
                prev_token = token
                continue

            if is_preposition(prev_token) or is_preposition(token):
                if is_preposition(token):
                    environment_features['preposition_between'] = 1
                if is_preposition(token):
                    environment_features['preposition_before'] = 1
                prev_token = token
                continue

            if is_punct(token):
                environment_features['punct_between'] = 1
                continue

            if token.value == ']':
                ground_truth = False
                for ft in environment_features:
                    environment_features[ft] = 0
                continue

            if not ground_truth:
                environment_features['preposition_before'] = 0

            token.chunked = ground_truth

            if prev_token.chunked and token.chunked:
                label = 1 if ground_truth else 0
            else:
                label = 0
            feature_vector = self._compute_features2(prev_token, token, environment_features)
            dataset.append((feature_vector, label))

            prev_token = token


    def train(self, samples, number_of_epochs=10, rand_seed=3, verbose=False):
        self.execution_timer.start()
        dataset = self.generate_dataset(samples)
        if verbose:
            self.execution_timer.show('preprocessing')

        self.execution_timer.start()
        self.fit(dataset, number_of_epochs=number_of_epochs, verbose=verbose)
        if verbose:
            print('')
            self.execution_timer.show('fitting')


    def fit(self, dataset, number_of_epochs, verbose=False):
        feature_vector_size = dataset[0][0].shape[0]
        network = FeedforwardNetwork(feature_vector_size, 2, (20, 20))
        network.fit(dataset, number_of_epochs=number_of_epochs)


    def _compute_features2(self, token1, token2, environment_features):
        features = []
        for ft in environment_features:
            features.append(float(environment_features[ft]))
        for pattern in feature_func_patterns:
            feature_value_1 = 1.0 if feature_func_patterns[pattern](token1) else 0.0
            feature_value_2 = 1.0 if feature_func_patterns[pattern](token2) else 0.0
            features.extend([feature_value_1, feature_value_2])

        return np.array(features)