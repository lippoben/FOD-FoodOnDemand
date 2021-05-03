import numpy as np
import pandas as pd

all_ingredients = pd.read_csv("NormalisedIngredients.csv")

random_ingredients_1 = all_ingredients["Ingredients"][0:50]
random_ingredients_1 = random_ingredients_1.to_numpy()
random_ingredients_1 = pd.DataFrame(random_ingredients_1, columns=['Ingredients'])

print(random_ingredients_1.shape)
print(type(random_ingredients_1))

all_ingredients = all_ingredients.drop(index=all_ingredients.index[:50])
random_ingredients_2 = all_ingredients.sample(n=50)
random_ingredients_2 = random_ingredients_2.to_numpy()
random_ingredients_2 = pd.DataFrame(random_ingredients_2, columns=['Ingredients'])

print(random_ingredients_2.shape)
print(type(random_ingredients_2))

random_ingredients = pd.concat([random_ingredients_1, random_ingredients_2])

print(random_ingredients.shape)
print(random_ingredients)

random_ingredients.to_csv("RandomIngredients.csv")
