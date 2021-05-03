import numpy as np
import itertools
import pandas as pd


np_load_old = np.load
np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)
with np.load('simplified-recipes-1M.npz') as data:
    recipes = data['recipes']
    ingredients = data['ingredients']

ingredients.astype(set)

# print(ingredients)
# print(len(ingredients))
#
# for i, val in enumerate(itertools.islice(ingredients, 100)):
#     print(val)

df = pd.DataFrame(ingredients, columns=['Ingredients'])
print(df)

df.to_csv('Ingredients.csv', index=False)
