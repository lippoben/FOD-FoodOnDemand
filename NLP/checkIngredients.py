from Webscraping import sqlDatabaseManagement as sql


def removeDuplicates(myList):
    return list(dict.fromkeys(myList))


# take the second element for sort
def takeThird(elem):
    return elem[2]


def checkIngredients(recipeDatabaseConn, userIngredientsArray, threshold=1):
    IDArray = sql.sqlGetCol(recipeDatabaseConn, "ID")
    possibleRecipesID = []
    for ID in IDArray:
        recipeCleanIngredients = sql.sqlGetSpecificID(recipeDatabaseConn, "CLEANINGREDIENTS", ID).split(", ")
        recipeSet = set(recipeCleanIngredients)
        userSet = set(userIngredientsArray)
        missingIngredients = recipeSet - userSet
        intersectionSet = set.intersection(recipeSet, userSet)
        recipeThreshold = len(intersectionSet)/len(recipeSet)
        if recipeThreshold >= threshold:
            possibleRecipesID.append([ID, missingIngredients, recipeThreshold])
    return sorted(possibleRecipesID, key=takeThird, reverse=True)

