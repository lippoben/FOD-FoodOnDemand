from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
import pandas as pd


def stemSentence(sentence):
    # used when cleaning and normalising ingredients
    wnl = WordNetLemmatizer()
    token_words = word_tokenize(sentence)
    stem_sentence = []
    for word in token_words:
        stem_sentence.append(wnl.lemmatize(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)


def normaliseIngredients(string):
    string = string.lower()
    string = re.sub("[^a-zA-Z ]+", "", string)
    string = stemSentence(string)
    return string


def cleanIngredients(dirtyIngredients):
    # pre load potential ingredients csv. used for cleaning and normalising ingredients
    allIngredients = pd.read_csv("normalisedIngredients.csv")
    splitIngredients = dirtyIngredients.split(",")
    cleanSplitIngredients = []
    normalisedIngredients = []

    for i in range(0, len(splitIngredients)):
        cleanSplitIngredients.append(normaliseIngredients(splitIngredients[i]))
        words = cleanSplitIngredients[i].split(" ")[:-1]
        longestWord = ""

        for j in range(0, len(words)):
            for k in range(0, len(words) - j):
                temp_words = ' '.join(words[j: len(words) - k])

                if len(allIngredients[allIngredients['Ingredients'] == temp_words]) > 0:
                    if longestWord == "" or len(temp_words.split(" ")) > len(longestWord.split(" ")):
                        longestWord = temp_words

        if longestWord != "":
            normalisedIngredients.append(longestWord)

    normalisedIngredients = set(normalisedIngredients)
    normalisedIngredients = list(normalisedIngredients)

    normalisedIngredients = str(normalisedIngredients)
    normalisedIngredients = normalisedIngredients.replace('[', '')
    normalisedIngredients = normalisedIngredients.replace(']', '')
    normalisedIngredients = normalisedIngredients.replace('\'', '')
    return normalisedIngredients
