import re
import os

import numpy as np
import pandas as pd
from scipy import spatial
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


def trainModel(model, corpusDir, epochs=30):
    corpusTextFileNameArray = os.listdir(corpusDir)
    corpusTextArray = []
    for corpusTextFileName in corpusTextFileNameArray:
        with open(corpusDir + corpusTextFileName, 'r') as f:
            corpusTextArray.append(f.read().split())

    corpus = Corpus()

    corpus.fit(corpusTextArray, window=10)

    model.fit(corpus.matrix, epochs=epochs, no_threads=4, verbose=False)
    model.add_dictionary(corpus.dictionary)
    return model


def findClosestEmbeddings(wordEmbeddings, embedding):
    return sorted(wordEmbeddings.keys(), key=lambda word: spatial.distance.euclidean(wordEmbeddings[word], embedding))


def removeStopWords():
    corpusTextFileNameArray = os.listdir('corpora/methodCorpus/')
    corpusTextArray = []
    for corpusTextFileName in corpusTextFileNameArray:
        with open('corpora/methodCorpus/' + corpusTextFileName, 'r') as f:
            text = f.read()
            corpusTextArray.append(text.split())
            textTokens = word_tokenize(text)
            textWithoutStopWords = [word for word in textTokens if not word in stopwords.words()]
            separator = ' '
            textWithoutStopWords = separator.join(textWithoutStopWords)
            f.close()

        with open('corpora/noStopwordsMethodCorpus/' + corpusTextFileName, 'w') as g:
            g.write(textWithoutStopWords)


def findNearestIngredients(wordEmbeddings, ingredient, cleanIngredients, maxIngredients=2):
    closestIngredientsArray = []
    try:
        closestEmbeddingsArray = findClosestEmbeddings(wordEmbeddings, wordEmbeddings[ingredient])[1:20]

        for closestEmbeddings in closestEmbeddingsArray:
            if closestEmbeddings in cleanIngredients:
                closestIngredientsArray.append(closestEmbeddings)
                # print(closestEmbeddings)

            if len(closestIngredientsArray) >= maxIngredients:
                return closestIngredientsArray

        return closestIngredientsArray

    except KeyError:
        print("no embedding for this ingredient skipping")
        return closestIngredientsArray


def formatWordEmbeddings(gloveModel):
    wordEmbeddings = gloveModel.dictionary

    for word in wordEmbeddings:
        wordEmbeddings[word] = gloveModel.word_vectors[gloveModel.dictionary[word]]

    return wordEmbeddings


def gloveInit():

    cleanIngredients = pd.read_csv('C:/Users/lipb1/Documents/Year 3 Bristol/MDM3/FOD/NLP/normalisedIngredients.csv')
    cleanIngredients = np.array(cleanIngredients['Ingredients'])
    gloveModel = Glove.load('C:/Users/lipb1/Documents/Year 3 Bristol/MDM3/FOD/GloVe/models/glove 400.txt')
    embeddings = formatWordEmbeddings(gloveModel)
    return embeddings, cleanIngredients


def queryGlove(embeddings, queryIngredient, cleanIngredientsArray):
    # print('Glove output for \'' + queryIngredient + '\'')
    return findNearestIngredients(embeddings, queryIngredient, cleanIngredientsArray, maxIngredients=3)


# trainModel('corpora/noStopwordsMethodCorpus/', 3)
'''
nearestIngredientsArray = []

modelTrained = False
epoch = 20
stepSize = 20
gloveModel = Glove(no_components=30, learning_rate=0.05)
# print('starting at epoch ' + str(epoch))
# gloveModel = Glove.load('models/glove ' + str(epoch) + '.txt')
while not modelTrained:
    print('\ntraining up to ' + str(epoch) + ' epochs')
    gloveModel = trainModel(gloveModel, 'corpora/noStopwordsMethodCorpus/', stepSize)
    gloveModel.save('models/glove ' + str(epoch) + '.txt')
    wordEmbeddings = gloveModel.dictionary

    for word in wordEmbeddings:
        wordEmbeddings[word] = gloveModel.word_vectors[gloveModel.dictionary[word]]

    newNearestIngredientsArray = findNearestIngredients()
    print(newNearestIngredientsArray)
    if newNearestIngredientsArray == nearestIngredientsArray:
        print('epoch: ')
        print(epoch)
        print(nearestIngredientsArray)
        modelTrained = True

    else:
        nearestIngredientsArray = newNearestIngredientsArray
        epoch += stepSize
'''
