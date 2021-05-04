from Webscraping import sqlDatabaseManagement as sql


def removeDuplicates(myList):
    return list(dict.fromkeys(myList))


def checkIngredients(recipeDatabaseConn, userIngredientsArray):
    IDArray = sql.sqlGetCol(recipeDatabaseConn, "ID")
    possibleRecipesID = []
    for ID in IDArray:
        recipeCleanIngredients = sql.sqlGetSpecificID(recipeDatabaseConn, "CLEANINGREDIENTS", ID)[0].split(", ")
        if set.issubset(set(recipeCleanIngredients), set(userIngredientsArray)):
            possibleRecipesID.append(ID)

    return possibleRecipesID

