import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
import numpy as np


def stemSentence(sentence):
    token_words = word_tokenize(sentence)
    stem_sentence = []
    for word in token_words:
        stem_sentence.append(wnl.lemmatize(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)


def normalise_ingredients(string):
    string = string.lower()
    string = re.sub("[^a-zA-Z ]+", "", string)
    string = stemSentence(string)
    return string


wnl = WordNetLemmatizer()

'''
ingredients_list = pd.read_csv("Ingredients.csv")
np_normalised_ingredients_list = np.zeros([2762, 1])
normalised_ingredients_list = pd.DataFrame(np_normalised_ingredients_list, columns=["Ingredients"])

print(ingredients_list["Ingredients"][2])
print(len(ingredients_list))

for i in range(0, len(ingredients_list)):
    normalised_ingredients_list["Ingredients"][i] = normalise_ingredients(ingredients_list["Ingredients"][i])

print(len(normalised_ingredients_list))
normalised_ingredients_list = normalised_ingredients_list.drop_duplicates()
print(len(normalised_ingredients_list))

normalised_ingredients_list.to_csv("normalised_ingredients.csv")
'''

recipes = pd.read_csv("RECIPESDATABASE.csv")
all_ingredients = pd.read_csv("normalised_ingredients.csv")
cleaned_ingredients = np.zeros([len(recipes), 1])
cleaned_ingredients = pd.DataFrame(cleaned_ingredients, columns=["Clean Ingredients"])
cleaned_ingredients = cleaned_ingredients.astype('object')

print(all_ingredients.head())

for h in range(0, len(recipes)):
    dirty_ingredients = recipes["INGREDIENTS"][h]
    split_ingredients = dirty_ingredients.split(",")
    clean_split_ingredients = []
    normalised_ingredients = []

    for i in range(0, len(split_ingredients)):
        clean_split_ingredients.append(normalise_ingredients(split_ingredients[i]))
        words = clean_split_ingredients[i].split(" ")[:-1]
        not_found_ingredient = False
        longest_word = ""

        for j in range(0, len(words)):
            for k in range(0, len(words) - j):
                temp_words = ' '.join(words[j: len(words) - k])
                print(all_ingredients[all_ingredients['Ingredients'] == temp_words])
                if len(all_ingredients[all_ingredients['Ingredients'] == temp_words]) > 0:
                    if longest_word == "" or len(temp_words.split(" ")) > len(longest_word.split(" ")):
                        longest_word = temp_words

        if longest_word != "":
            normalised_ingredients.append(longest_word)

    normalised_ingredients = set(normalised_ingredients)
    normalised_ingredients = list(normalised_ingredients)

    cleaned_ingredients["Clean Ingredients"][h] = normalised_ingredients
    if h % 100 == 0:
        print(h)


# cleaned_ingredients.to_csv("clean_ingredients.csv")

print(np.shape(cleaned_ingredients))

# print(clean_split_ingredients, '\n')
# print(normalised_ingredients, '\n')
#
# print(cleaned_ingredients.head())
#
# print(recipes.head())
#
# print(dirty_ingredients)
