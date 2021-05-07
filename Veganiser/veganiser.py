import pandas as pd
from Webscraping import sqlDatabaseManagement as sql
from difflib import SequenceMatcher


# sequence matcher,
def similar(a, b):
    ratio = SequenceMatcher(None, a, b).ratio()
    matches = a, b
    return ratio, matches


# splitting the titles into lists
def titleList(r):
    word_list = r.split(' ')
    S = set(word_list)
    ing_list = list(S)
    return ing_list


# splitting the ingredients into lists
def ingredientsList(r):
    word_list = r.split(', ')
    S = set(word_list)
    ing_list = list(S)
    return ing_list


# removing words from the title
def removeTitle(t):
    word = titleList(t)
    for s in word:
        N = 'vegan quick'
        N = titleList(N)
        for c in N:
            if s == c:
                word.remove(s)
    return word


# removing non vegan words from the ingredients
def remove(t):
    words = ingredientsList(t)
    for s in words:
        # will add more ingredients, as right now a very random selection
        N = 'fish, egg, chicken, beef, lamb, duck, pork, salmon fillet, egg yolk, skinless chicken breast, leg of lamb, chicken thigh,'
        N = ingredientsList(N)
        for c in N:
            if s == c:
                words.remove(s)
    return words


# input recipe name from other_df, iterate through titles in vegan_df, if ratio >0.9 print recipe name
# else go through the clean ingredients


def veganise(recipeDatabase, recipeID, titleMatchThreshHold=0.8, ingredientsMatchThreshold=0.5):
    recipeName = sql.sqlGetSpecificID(recipeDatabase, 'RECIPENAME', recipeID)
    recipeIngredients = sql.sqlGetSpecificID(recipeDatabase, 'CLEANINGREDIENTS', recipeID)
    recipeIngredients = remove(recipeIngredients)
    veganRecipeIDArray = sql.sqlGetAllVeganRecipes(recipeDatabase)
    nonVeganRecipeIDArray = sql.sqlGetAllNonVeganRecipes(recipeDatabase)
    possibleAlternativeVeganRecipeArray = []

    # putting everything in lower case so it matches
    lowerCaseRecipeName = recipeName.lower()
    lowerCaseRecipeName = removeTitle(lowerCaseRecipeName)

    for veganRecipeID in veganRecipeIDArray:
        veganRecipeName = sql.sqlGetSpecificID(recipeDatabase, 'RECIPENAME', veganRecipeID)
        lowerCaseVeganRecipeName = veganRecipeName.lower()
        noVeganTitleLowerCaseVeganRecipeName = removeTitle(lowerCaseVeganRecipeName)
        percentageTitleMatch = similar(lowerCaseRecipeName, noVeganTitleLowerCaseVeganRecipeName)[0]
        if percentageTitleMatch >= titleMatchThreshHold:
            possibleAlternativeVeganRecipeArray.append(veganRecipeID)
        else:
            veganRecipeIngredients = sql.sqlGetSpecificID(recipeDatabase, 'CLEANINGREDIENTS', veganRecipeID).split(', ')
            percentageIngredientMatch = similar(recipeIngredients, veganRecipeIngredients)[0]
            if percentageIngredientMatch >= ingredientsMatchThreshold:
                possibleAlternativeVeganRecipeArray.append(veganRecipeID)

            else:
                continue

    return possibleAlternativeVeganRecipeArray
