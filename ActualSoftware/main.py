import numpy as np
import pandas as pd
from pprint import pprint
from Webscraping import sqlDatabaseManagement as sql
from Veganiser.veganiser import veganise
from NLP.checkIngredients import checkIngredients
from NLP.ingredientNormliser import cleanIngredients

# establish connection to database
recipeDatabaseConn = sql.sqlInit('recipeDatabase.db')

# this will be what the user has in stock
# userInput = np.array(['potatoes', 'olives oil'])
userInput = pd.read_csv('C:/Users/lipb1/Documents/Year 3 Bristol/MDM3/FOD/NLP/normalisedIngredients.csv').head(50)
userInput = np.array(userInput['Ingredients'])

# normalise and clean users input
normalisedUserInput = cleanIngredients(userInput)

# Green light recipes here
greenLitRecipesIDArray = checkIngredients(recipeDatabaseConn, normalisedUserInput)
# output green lit recipes for funzys
for greenLitRecipeID in greenLitRecipesIDArray:
    greenLitRecipeName = sql.sqlGetSpecificID(recipeDatabaseConn, 'RECIPENAME', greenLitRecipeID)
    greenLitRecipeURL = sql.sqlGetSpecificID(recipeDatabaseConn, 'URL', greenLitRecipeID)
    greenLitRecipeIngredients = sql.sqlGetSpecificID(recipeDatabaseConn, 'CLEANINGREDIENTS', greenLitRecipeID)
    greenLitRecipeMethod = sql.sqlGetSpecificID(recipeDatabaseConn, 'METHOD', greenLitRecipeID)

    # Check Green lit recipes here against user's preference profile and select the recipes that best match

    # Veganise Recipes
    possibleVeganAlternativeIDArray = veganise(recipeDatabaseConn, greenLitRecipeName)

    # Display output to the user
    print(greenLitRecipeID)
    print(greenLitRecipeURL)
    print(greenLitRecipeName)
    print(greenLitRecipeIngredients)
    pprint(greenLitRecipeMethod)

    if len(possibleVeganAlternativeIDArray) >= 2:
        print('\nList of possible vegan alternatives: ')
        for possibleVeganAlternativeID in possibleVeganAlternativeIDArray:
            possibleVeganAlternativeRecipeName = sql.sqlGetSpecificID(recipeDatabaseConn,
                                                                      'RECIPENAME', possibleVeganAlternativeID)

            if possibleVeganAlternativeID != greenLitRecipeID:
                print(possibleVeganAlternativeID)
                print(possibleVeganAlternativeRecipeName)

    print('\n')

