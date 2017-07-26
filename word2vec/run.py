#import nltk
from collections import Counter
from tokenizer import Tokenizer

#nltk.download()
#tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

tokenizer = Tokenizer()
words = []

with open("sample.txt", 'r', encoding='utf-8') as file:
    lines = file.read().lower()

    for line in tokenizer.split_into_sentences(lines):
        words += tokenizer.split_into_words(line)

counts = Counter(words)
print(counts)