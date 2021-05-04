import json, re
import pandas as pd, numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
ps = PorterStemmer()

recipe_names = []
ingredient_sets = []
file = r'jsonrecipes.json'
data = pd.read_json('jsonrecipes.json')
print(data.keys())
with open(file, encoding='utf-8') as train_file:
    recipe_set = json.load(train_file)
    for recipe in recipe_set:
        ingredients = recipe["CLEANINGREDIENTS"].split(', ')
        ingredient_sets.append(ingredients)
        recipe_names.append(recipe["RECIPENAME"])


#Make dataframe of names and respective clean ingredients
df = pd.DataFrame({'Name':recipe_names,
                   'ingredients':ingredient_sets})

new = []
for s in df['ingredients']:
    s = ' '.join(s)
    new.append(s)

df['ing'] = new

l=[]
for s in df['ing']:

    #Remove punctuations
    s=re.sub(r'[^\w\s]','',s)

    #Remove Digits
    s=re.sub(r"(\d)", "", s)

    #Remove content inside paranthesis
    s=re.sub(r'\([^)]*\)', '', s)

    #Remove Brand Name
    s=re.sub(u'\w*\u2122', '', s)


    #Convert to lowercase
    s=s.lower()

    #Remove Stop Words
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(s)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    s = ' '.join(filtered_sentence)

    #Remove low-content adjectives


    #Porter Stemmer Algorithm
    words = word_tokenize(s)
    word_ps = []
    for w in words:
        word_ps.append(ps.stem(w))
    s = ' '.join(word_ps)

    l.append(s)


#^^^Modifies ingredients list by stemming words for comparison
#In future could account for titles as they include useful data
df['ing_mod'] = l
tfidf = TfidfVectorizer(
    min_df = 5,
    max_df = 0.95,
    max_features = 8000,
    stop_words = 'english'
)
tfidf.fit(data.CLEANINGREDIENTS)
# text = tfidf.transform(l.contents)

#TFIDF vectoriser gives weighting to each word respective of it's occurences in each data set(ie ingredients list)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['ing_mod'])

clusters = KMeans(init='k-means++', n_clusters=8).fit_predict(X)
#Clusters ingredients sets
print(len(clusters))


def plot_tsne_pca(data, labels):
    max_label = max(labels)
    max_items = np.random.choice(range(data.shape[0]), size=3000, replace=False)

    pca = PCA(n_components=2).fit_transform(data[max_items,:].todense())
    tsne = TSNE().fit_transform(PCA(n_components=50).fit_transform(data[max_items,:].todense()))


    idx = np.random.choice(range(pca.shape[0]), size=300, replace=False)
    label_subset = labels[max_items]
    label_subset = [cm.hsv(i/max_label) for i in label_subset[idx]]

    f, ax = plt.subplots(1, 2, figsize=(14, 6))

    ax[0].scatter(pca[idx, 0], pca[idx, 1], c=label_subset)
    ax[0].set_title('PCA Cluster Plot')

    ax[1].scatter(tsne[idx, 0], tsne[idx, 1], c=label_subset)
    ax[1].set_title('TSNE Cluster Plot')


result = pd.DataFrame({'Name': recipe_names,
                       'Cluster': clusters})
print(result.head(50))
# sorteddf = result.sort_values(by='Cluster')
# print(sorteddf.head(15))
plot_tsne_pca(X, clusters)
plt.show()
