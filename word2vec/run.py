#import nltk
from collections import Counter
from tokenizer import Tokenizer

#nltk.download()
#tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

tokenizer = Tokenizer()
words = []
sentences = []
with open("sample.txt", 'r', encoding='utf-8') as file:
    lines = file.read().lower()
    sentences = tokenizer.split_into_sentences(lines)
    for line in sentences:
        words += tokenizer.split_into_words(line)

counts = Counter(words)
window_size = 3

word_pair_frequences = {}
for sent in sentences:
    words = tokenizer.split_into_words(sent)
    for word_position in range(len(words)):
        word = words[word_position]

        if not word in word_pair_frequences:
            word_pair_frequences[word] = []

        start_pos = max(0, word_position - window_size)
        end_pos = min(len(words) - 1, word_position + window_size)
        for second_word_position in range(start_pos, end_pos):
            second_word = words[second_word_position]

            if second_word != word:
                word_pair_frequences[word].append(second_word)

for key in word_pair_frequences.keys():
    word_pair_frequences[key] = Counter(word_pair_frequences[key])

print(word_pair_frequences)