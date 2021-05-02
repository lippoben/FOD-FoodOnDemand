import numpy as np
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import sqlDatabaseManagement as sql
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# https://www.bbcgoodfood.com/recipes/category Category = Collections
# https://www.bbcgoodfood.com/recipes/collection/quick-and-healthy-recipes/ Collections = Recipes
# https://www.bbcgoodfood.com/recipes/chicken-satay-salad Recipes = Profit


def contains(substring, string):
    if string.lower is not None:
        if substring.lower() in string.lower():
            return True
        else:
            return False

    else:
        return False


def removeDuplicates(myList):
    return list(dict.fromkeys(myList))


def stemSentence(sentence):
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


def scrapeRecipeName(recipeNameSoup):
    for tag in recipeNameSoup:
        recipeNameString = str(tag.text)

    recipeNameString = recipeNameString.replace('\'', '')

    return recipeNameString


def cleanIngredients(dirtyIngredients):
    split_ingredients = dirtyIngredients.split(",")
    cleanSplitIngredients = []
    normalisedIngredients = []

    for i in range(0, len(split_ingredients)):
        cleanSplitIngredients.append(normaliseIngredients(split_ingredients[i]))
        words = cleanSplitIngredients[i].split(" ")[:-1]
        longest_word = ""

        for j in range(0, len(words)):
            for k in range(0, len(words) - j):
                temp_words = ' '.join(words[j: len(words) - k])

                if len(all_ingredients[all_ingredients['Ingredients'] == temp_words]) > 0:
                    if longest_word == "" or len(temp_words.split(" ")) > len(longest_word.split(" ")):
                        longest_word = temp_words

        if longest_word != "":
            normalisedIngredients.append(longest_word)

    normalisedIngredients = set(normalisedIngredients)
    normalisedIngredients = list(normalisedIngredients)

    normalisedIngredients = str(normalisedIngredients)
    normalisedIngredients = normalisedIngredients.replace('[', '')
    normalisedIngredients = normalisedIngredients.replace(']', '')
    normalisedIngredients = normalisedIngredients.replace('\'', '')
    return normalisedIngredients


def scrapeIngredients(ingredientsSoup):
    ingredientsArrayString = []
    for li_tag in ingredientsSoup:
        ingredientsArrayString.append(li_tag.text)

    ingredientsArrayString = str(ingredientsArrayString)
    ingredientsArrayString = ingredientsArrayString.replace('[', '')
    ingredientsArrayString = ingredientsArrayString.replace(']', '')
    ingredientsArrayString = ingredientsArrayString.replace('\'', '')

    return ingredientsArrayString


def scrapeVeganTag(tagsSoup):
    infoTagsArrayString = []
    for tag in tagsSoup:
        if str(tag.text) == ('Vegan' or 'vegan'):
            infoTagsArrayString.append(str(tag.text))

    infoTagsArrayString = str(infoTagsArrayString)
    infoTagsArrayString = infoTagsArrayString.replace('[', '')
    infoTagsArrayString = infoTagsArrayString.replace(']', '')
    infoTagsArrayString = infoTagsArrayString.replace('\'', '')

    return infoTagsArrayString


def scrapeMethod(methodTableSoup):
    methodTextHTML = methodTableSoup.find_all('div', class_='editor-content')

    methodArrayString = []
    for li_tag in methodTextHTML:
        methodArrayString.append(li_tag.text)

    methodArrayString = str(methodArrayString)
    methodArrayString = methodArrayString.replace('[', '')
    methodArrayString = methodArrayString.replace(']', '')
    methodArrayString = methodArrayString.replace('\'', '')

    return methodArrayString


# create/connect to the recipe database
connection = sql.sqlInit("recipeDatabase.db")

# pre load potential ingredients csv. used for cleaning and normalising ingredients
all_ingredients = pd.read_csv("normalised_ingredients.csv")

# used when cleaning and normalising ingredients
wnl = WordNetLemmatizer()

# creates the table in the database. WARNING: this line only needs to be run once after a new database is created
#                                             so comment out if connecting to pre-existing database
sql.sqlCreateTable(connection)

primaryKeyId = 1


rootURL = 'https://www.bbcgoodfood.com/recipes/category'
linksToExplore = [rootURL]

linksExplored = []
while linksToExplore:
    for link in linksToExplore:

        if link in linksExplored:
            # Link already explored. Remove and skip link
            linksToExplore.remove(link)

        else:
            response = requests.get(link)
            # print('Visited URL: {}'.format(response.url))
            # print(response.status_code)
            # if the link was accessed successfully then explore it.
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                dataContainers = soup.find_all('a', class_="standard-card-new__article-title qa-card-link")
                if not dataContainers:

                    recipeName = scrapeRecipeName(soup.find_all('h1', class_='post-header__title post-header__title--masthead-layout heading-1'))
                    ingredientsArray = scrapeIngredients(soup.find_all('li', class_='pb-xxs pt-xxs list-item list-item--separator'))
                    cleanIngredientsArray = cleanIngredients(ingredientsArray)
                    infoTagsArray = scrapeVeganTag(soup.find_all('div', class_='icon-with-text icon-with-text--aligned'))
                    methodArray = scrapeMethod(soup.find('ul', class_='grouped-list__list list'))
                    linkString = str(link).replace('\'', '')

                    # sql.sqlInsertRecords(connection, primaryKeyId, recipeName, ingredientsArray, infoTagsArray)
                    sql.sqlInsertRecords(connection, primaryKeyId, linkString, recipeName, ingredientsArray, cleanIngredientsArray, methodArray, infoTagsArray)
                    sql.sqlCommit(connection)
                    primaryKeyId += 1

                else:
                    # We need to go deeper to find recipes pages
                    # get all the links on this page
                    collectionLinkArray = []
                    for href in dataContainers:
                        linksToExplore.append(href.get('href'))

                    # find all the other pages don't worry about dupes they get filtered out by 'linksExplored' list
                    dataContainers = soup.find_all('a', class_="pagination-item")
                    for href in dataContainers:
                        if href.get('href')[0] != 'h':
                            linksToExplore.append("https://www.bbcgoodfood.com" + href.get('href'))

                        else:
                            linksToExplore.append(href.get('href'))

                if primaryKeyId % 101 == 0:
                    print("Recipes Found: " + str(primaryKeyId - 1))
                    print("Links left to explore: " + str(len(linksToExplore)) + "\n")

                # store explored links and remove the explored link from links to be explored
                linksExplored.append(link)
                linksToExplore.remove(link)

                # remove any duplicated appended links to improve run time
                removeDuplicates(linksToExplore)
                removeDuplicates(linksExplored)

            # if the url didn't give a response then skip for now and revisit later.
            else:
                print('Attempted to visit URL: {}'.format(response.url))
                print("Failed to access url.\n")
                linksExplored.append(link)
                linksToExplore.remove(link)

sql.sqlPrintAll(connection)
print("Recipes Found: " + str(primaryKeyId - 1))
sql.sqlClose(connection)
