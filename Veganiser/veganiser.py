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


def veganise(recipeDatabase, recipeName):
    veganRecipeIDArray = sql.sqlGetAllVeganRecipes(recipeDatabase)
    nonVeganRecipeIDArray = sql.sqlGetAllNonVeganRecipes(recipeDatabase)

    # rowRecipe = (other_df[other_df['RECIPENAME'] == recipeName])

    # putting everything in lower case so it matches
    lowerCaseRecipeName = recipeName.lower()
    lowerCaseRecipeName = removeTitle(lowerCaseRecipeName)
    # recipeCleanIngredients = rowRecipe['CLEANINGREDIENTS']

    for veganRecipeID in veganRecipeIDArray:
        veganRecipeName = sql.sqlGetSpecificID(recipeDatabase, 'RECIPENAME', veganRecipeID)
        lowerCaseVeganRecipeName = veganRecipeName.lower()
        noVeganTitleLowerCaseVeganRecipeName = removeTitle(lowerCaseVeganRecipeName)
        percentageTitleMatch = similar(lowerCaseRecipeName, noVeganTitleLowerCaseVeganRecipeName)[0]
        if percentageTitleMatch >= 0.8:
            # veganRecipe = (vegan_df[vegan_df['RECIPENAME'] == veganRecipeName])
            print('Here is an alternative vegan recipe: ', veganRecipeName)
        else:
            # Here is where we will then go into the ingredients
            '''
            for o in vegan_df['CLEANINGREDIENTS']:
                o=remove(o)
                M = (similar(n,o))
                if M[0] >= 0.5:
                print(M)
                print(i)
            '''
            continue

