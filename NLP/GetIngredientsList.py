import json
import re

df1 = open('test.json')
df2 = open('train.json')

ds1 = json.load(df1)
ds2 = json.load(df2)

print(ds1[9900]['ingredients'][0])
print(len(ds1))

ingredients = set()

for i in range(0, len(ds2)):
    for j in range(0, len(ds2[i]['ingredients'])):
        ingredient = ds2[i]['ingredients'][j].lower()
        ingredient = re.sub("[^a-zA-Z ]+", "", ingredient)
        ingredients.add(ingredient)

print(ingredients)
