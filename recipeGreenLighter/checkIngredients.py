import numpy as np
import pandas as pd
from webscraping import sqlDatabaseManagement as sql


def removeDuplicates(myList):
    return list(dict.fromkeys(myList))


def checkIngredients(recipeDatabaseConn, userIngredientsDf):
    IDArray = sql.sqlGetCol(recipeDatabaseConn, "ID")
    possibleRecipesID = []

    for ID in IDArray:
        cleanIngredients = sql.sqlGetSpecificID(recipeDatabaseConn, "CLEANINGREDIENTS", ID)[0].split(", ")
        for j in range(0, len(cleanIngredients)):
            if len(userIngredientsDf[userIngredientsDf['Ingredients'] == cleanIngredients[j]]) == 0:
                break
            possibleRecipesID.append(ID)

    possibleRecipesID = removeDuplicates(possibleRecipesID)

    print(possibleRecipesID)
    print(len(possibleRecipesID))

