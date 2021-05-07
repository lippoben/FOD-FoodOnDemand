import pandas as pd
import numpy as np
from difflib import SequenceMatcher

data = pd.read_csv('TRIAL2.csv')
vegan_df = data[data['INFOTAGS'] == 'Vegan']
other_df=data[data['INFOTAGS'] != 'Vegan']

#sequence matcher,
def similar(a,b):
    ratio = SequenceMatcher(None, a, b).ratio()
    overlap = SequenceMatcher(None, a, b).get_matching_blocks()
    matches = a, b
    return ratio, matches, overlap

#spliting the titles into lists
def title_list(r):
    word_list = r.split(' ')
    S = set(word_list)
    ing_list = list(S)
    return ing_list


#splitting the ingredients into lists
def ingredients_list(r):
    word_list = r.split(', ')
    S = set(word_list)
    ing_list = list(S)
    return ing_list

#removing words from the title
def remove_title(t):
    word = title_list(t)
    for s in word:
        N= ('vegan quick')
        N = title_list(N)
        for c in N:
            if s == c:
                word.remove(s)
    return word

#removing non vegan words from the ingredients
def remove(t):
    words = t
    #words = ingredients_list(t)
    for s in words:
        #will add more ingredients, as right now a very random selection
        N= ('fish, egg, chicken, beef, lamb, duck, pork, salmon fillet, egg yolk, skinless chicken breast, leg of lamb, chicken thigh,')
        N = ingredients_list(N)
        for c in N:
            if s == c:
                words.remove(s)
    return words


#input recipe name from other_df, iterate through titles in vegan_df, if ratio >0.9 print recipe name, else go through the clean ingredients

a = input('Enter recipe: ')
rowrecipe= (other_df[other_df['RECIPENAME'] == a])


#putting everything in lower case so it matches
b = a.lower()
b = remove_title(b)
n= rowrecipe['CLEANINGREDIENTS']
n = n.to_string(index=False)

counter=0
for i in vegan_df['RECIPENAME']:
    i = str(i)
    j = i.lower()
    c = remove_title(j)
    d = similar(b,c)
    if d[0] >= 0.7:
        #print(d)
        veganrecipe = (vegan_df[vegan_df['RECIPENAME']== i]) #so we can also print the ingredients or method, whatever we want the output to be
        print('Here is an alternative vegan recipe: ', i)
        counter +=1
    else:
        continue

counter2= 0
overlapingredients=[]
if counter == 0:
    for o in vegan_df['CLEANINGREDIENTS']:
        n=remove(n)
        m=similar(n,o)
        if m[0] >= 0.5:
            veganrecipe = (vegan_df[vegan_df['CLEANINGREDIENTS']== o])
            p= (veganrecipe['RECIPENAME']).to_string(index=False)
            print('Here is an alternative vegan recipe: ', p)
            counter2 += 1
           # n=n.split()
           # print(type(n))
            #o = str(o)
           # o=o.split()
           # print(type(o))
           # for z in n:
           #     for y in o:
           #         if z == y:
           #             print(z)
           #             overlapingredients += z
          #          else:
          #              continue
            #for match in m[2]:
             #   overlap= n[match.a:match.a + match.size]
             #   n = str.split(', ' )
              #  for z in n:
              #      if overlap == z:
              #          overlapingredients += overlap
           # print("Overlapping ingredients: " , overlapingredients)
           # #print("Overlapping ingredients: ",m[2])
            #counter2 += 1
        else:
            continue

if counter2 == 0:
    print('No recipe found')
    #M = (similar(n,o) for o in vegan_df['CLEANINGREDIENTS'])
   # if M[0] >= 0.5:
     #   print(M)




#for i in other_df['RECIPENAME']:

#    M = (max(similar(i,j) for j in vegan_df['RECIPENAME']))
 #   print(M)
#    R += M

#if counter2 == 0:
 #   print('No vegan alternate to this recipe')
