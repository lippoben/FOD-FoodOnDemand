import numpy as np
import pandas as pd
from webscraping import sqlDatabaseManagement as sql


def removeDuplicates(myList):
    return list(dict.fromkeys(myList))


HomeIngredients = pd.read_csv("RandomIngredients.csv")
conn = sql.sqlInit("C:/Users/charl/PycharmProjects/NLP3/FOD-FoodOnDemand/NLP/recipeDatabase.db")
idarray = sql.sqlGetCol(conn, "ID")


possible_recipes_id = []

for i in idarray:
    clean_ingredients = sql.sqlGetSpecificID(conn, "CLEANINGREDIENTS", i)[0].split(", ")
    for j in range(0, len(clean_ingredients)):
        if len(HomeIngredients[HomeIngredients['Ingredients'] == clean_ingredients[j]]) == 0:
            break
        possible_recipes_id.append(i)

possible_recipes_id = removeDuplicates(possible_recipes_id)

print(possible_recipes_id)
print(len(possible_recipes_id))




