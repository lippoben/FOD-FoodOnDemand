import numpy as np
import pandas as pd
from pprint import pprint
from webscraping import sqlDatabaseManagement as sql
# from Veganiser import veganiser
from NLP.checkIngredients import checkIngredients
from NLP.ingredientNormliser import normaliseIngredients

# establish connection to database
recipeConn = sql.sqlInit('recipeDatabase.db')

# this will be what the user has in stock
userInput = np.array(['egg', 'potato', 'olive oil'])
# userInput = normaliseIngredients(userInput)

# Green light recipes here
greenLitRecipesArray = checkIngredients(recipeConn, userInput)
for greenLitRecipes in greenLitRecipesArray:
    print(sql.sqlGetSpecificID(recipeConn, 'RECIPENAME', greenLitRecipes)[0])
    print(sql.sqlGetSpecificID(recipeConn, 'CLEANINGREDIENTS', greenLitRecipes)[0])
    pprint(sql.sqlGetSpecificID(recipeConn, 'METHOD', greenLitRecipes)[0])
    print('\n')


# Check Green lit recipes here against user's preference profile and select the recipes that best match


# Veganise Recipes


# Display output to the user

