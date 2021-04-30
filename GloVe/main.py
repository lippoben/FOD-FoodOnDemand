import re
import os
import webscraping.sqlDatabaseManagement as sql
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.test.utils import common_texts
import gensim.models
from glove import glove, Corpus


def stemSentence(sentence):
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


wnl = WordNetLemmatizer()
conn = sql.sqlInit('C:/Users/lipb1/Documents/Year 3 Bristol/MDM3/FOD/webscraping/recipeDatabase.db')
file = open('C:/Users/lipb1/Documents/Year 3 Bristol/MDM3/FOD/GloVe/corpora/methodCorpus/methodSentence1.txt', 'r')

print(file.read().split())

model = gensim.models.Word2Vec(sentences=common_texts, window=5, min_count=1, workers=4)
print(model)
