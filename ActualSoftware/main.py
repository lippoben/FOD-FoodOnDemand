import numpy as np
from pprint import pprint
from Webscraping import sqlDatabaseManagement as sql
from Veganiser.veganiser import veganise
from NLP.checkIngredients import checkIngredients
from NLP.ingredientNormliser import cleanIngredients

# establish connection to database
recipeDatabaseConn = sql.sqlInit('recipeDatabase.db')

# this will be what the user has in stock
userInput = ['peppers', 'chickpeas', 'soy sauce', 'onion', 'salt', 'pepper', 'Bread', 'basmati rice', 'garlic']
userInputting = True
while userInputting:
    isUserDone = input('If you are finished type Y else type N: ')
    if isUserDone == 'Y':
        userInputting = False
    else:
        userInput.append(input('Please input 1 ingredient: '))
        print(userInput)

    print('\n')

userInput = np.array(userInput)
# userInput = pd.read_csv('C:/Users/lipb1/Documents/Year 3 Bristol/MDM3/FOD/NLP/normalisedIngredients.csv').head(50)
# userInput = np.array(userInput['Ingredients'])

# normalise and clean users input
normalisedUserInput = cleanIngredients(userInput)
print(normalisedUserInput)

# Green light recipes here
greenLitRecipesIDArray = checkIngredients(recipeDatabaseConn, normalisedUserInput, threshold=0.4)
# output green lit recipes for funzys
for greenLitRecipeID, greenLitRecipeMissingIngredients, threshold in greenLitRecipesIDArray:
    greenLitRecipeName = sql.sqlGetSpecificID(recipeDatabaseConn, 'RECIPENAME', greenLitRecipeID)
    greenLitRecipeURL = sql.sqlGetSpecificID(recipeDatabaseConn, 'URL', greenLitRecipeID)
    greenLitRecipeIngredients = sql.sqlGetSpecificID(recipeDatabaseConn, 'CLEANINGREDIENTS', greenLitRecipeID)
    greenLitRecipeMethod = sql.sqlGetSpecificID(recipeDatabaseConn, 'METHOD', greenLitRecipeID)

    # Check Green lit recipes here against user's preference profile and select the recipes that best match

    # Veganise Recipes
    possibleVeganAlternativeIDArray = veganise(recipeDatabaseConn, greenLitRecipeName)

    # Display output to the user
    print('ID: ' + str(greenLitRecipeID))
    print('URL: ' + greenLitRecipeURL)
    print('Recipe Name: ' + greenLitRecipeName)
    print("Percentage of matching ingredients: " + str(round(threshold*100)))
    print("\nList of missing ingredients:")
    for missingIngredients in greenLitRecipeMissingIngredients:
        print("     " + missingIngredients)

    print("\nList of recipe ingredients:")
    for recipeIngredients in greenLitRecipeIngredients.split(', '):
        print("     " + recipeIngredients)
    print("\nMethod:")
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

