import pandas as pd 
import numpy as np 
from difflib import SequenceMatcher

data= pd.read_csv('recipeDatabase.csv')
vegan_df=data[data['INFOTAGS']=='Vegan']
other_df=data[data['INFOTAGS']!='Vegan']

def ingredients(r):
    word_list = r.split(', ')
    S = set(word_list)
    ing_list = list(S)
    return ing_list

#all unique ingredients 
unique = []
for i in other_df['CLEANINGREDIENTS']:
    for x in ingredients(i):
        if x not in unique:
            unique.append(x)
    print(unique)       
    
#unique = sorted(unique)
#print(unique)

#non vegan ingredients
non_vegan = ['chicken', 'beef', 'egg', 'pork', 'chicken breast']
#non vegan ingredients that can easily be substituted
easy_vegan = ['milk', 'butter', 'honey', 'yogurt', 'cream cheese']


#outputting which recipes are non vegan, can be vegan or vegan 
for i in other_df['CLEANINGREDIENTS']:
    check = any(item in non_vegan for item in ingredients(i))
    ish = any(item in easy_vegan for item in ingredients(i))

    if check is False and ish is False:
        print("{} is vegan" .format(ingredients(i)))

    if check is False and ish is True:
        print("{} can easily be vegan" .format(ingredients(i)))

    if check is True:
        print("{} isn't vegan" .format(ingredients(i)))



