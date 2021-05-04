import pandas as pd
from difflib import SequenceMatcher

data = pd.read_csv('TRIAL2.csv')
vegan_df = data[data['INFOTAGS'] == 'Vegan']
other_df = data[data['INFOTAGS'] != 'Vegan']


# sequence matcher,
def similar(a, b):
    ratio = SequenceMatcher(None, a, b).ratio()
    matches = a, b
    return ratio, matches


# splitting the titles into lists
def title_list(r):
    word_list = r.split(' ')
    S = set(word_list)
    ing_list = list(S)
    return ing_list


# splitting the ingredients into lists
def ingredients_list(r):
    word_list = r.split(', ')
    S = set(word_list)
    ing_list = list(S)
    return ing_list


# removing words from the title
def remove_title(t):
    word = title_list(t)
    for s in word:
        N = 'vegan quick'
        N = title_list(N)
        for c in N:
            if s == c:
                word.remove(s)
    return word


# removing non vegan words from the ingredients
def remove(t):
    words = ingredients_list(t)
    for s in words:
        # will add more ingredients, as right now a very random selection
        N = 'fish, egg, chicken, beef, lamb, duck, pork, salmon fillet, egg yolk, skinless chicken breast, leg of lamb, chicken thigh,'
        N = ingredients_list(N)
        for c in N:
            if s == c:
                words.remove(s)
    return words


# input recipe name from other_df, iterate through titles in vegan_df, if ratio >0.9 print recipe name, else go through the clean ingredients

a = input('Enter recipe: ')
rowrecipe = (other_df[other_df['RECIPENAME'] == a])


# putting everything in lower case so it matches
b = a.lower()
b = remove_title(b)
n = rowrecipe['CLEANINGREDIENTS']

for i in vegan_df['RECIPENAME']:
    i = str(i)
    j = i.lower()
    c = remove_title(j)
    d = similar(b,c)
    if d[0] >= 0.8:
        # print(d)
        # so we can also print the ingredients or method, whatever we want the output to be
        veganrecipe = (vegan_df[vegan_df['RECIPENAME'] == i])
        print('Here is an alternative vegan recipe: ', i)
    else:
        # Here is where we will then go into the ingredients
        continue
        #for o in vegan_df['CLEANINGREDIENTS']:
         #   o=remove(o)
        #    M = (similar(n,o))
            #if M[0] >= 0.5:
         #   print(M)
        #    print(i)
