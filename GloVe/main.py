import re
import os

import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.test.utils import common_texts
import gensim.models
from glove import Glove, Corpus


def stemSentence(sentence):
    wnl = WordNetLemmatizer()
    token_words = word_tokenize(sentence)
    stem_sentence_var = []
    for word in token_words:
        stem_sentence_var.append(wnl.lemmatize(word))
        stem_sentence_var.append(" ")
    return "".join(stem_sentence_var)


def normaliseIngredients(string):
    string = string.lower()
    string = re.sub('[^a-zA-Z ]+', "", string)
    string = stemSentence(string)
    return string


def getUniqueWords(sentence):
    return sentence.split()


def trainModel():
    corpusTextFileNameArray = os.listdir('corpora/methodCorpus/')
    corpusTextArray = []
    for corpusTextFileName in corpusTextFileNameArray:
        with open('corpora/methodCorpus/' + corpusTextFileName, 'r') as f:
            corpusTextArray.append(f.read().split())

    corpus = Corpus()

    corpus.fit(corpusTextArray, window=10)

    glove = Glove(no_components=5, learning_rate=0.05)
    glove.fit(corpus.matrix, epochs=30, no_threads=4, verbose=True)
    glove.add_dictionary(corpus.dictionary)
    glove.save('glove.txt')


# trainModel()
corpusTextFileNameArray = os.listdir('corpora/methodCorpus/')
corpusTextArray = []
for corpusTextFileName in corpusTextFileNameArray:
    with open('corpora/methodCorpus/' + corpusTextFileName, 'r') as f:
        text = f.read()
        corpusTextArray.append(text.split())
        textTokens = word_tokenize(text)
        print(textTokens)
        textWithoutStopWords = [word for word in textTokens if not word in stopwords.words()]
        print(textWithoutStopWords)
        print("\n")

model = Glove.load('glove.txt')
print(model.word_vectors[model.dictionary['potato']])

