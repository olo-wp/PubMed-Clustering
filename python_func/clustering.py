from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.preprocessing import StandardScaler


def vectorize(data):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data["text"])
    tfidf_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    X = pd.concat([data, tfidf_df], axis=1)
    X = X.drop("text", axis=1)

    return X


def get_Clusters2(df, n_clusters=4):
    X = df.drop(["GEO", "PMID"], axis=1, inplace=False)

    standardScaler = StandardScaler()
    X = standardScaler.fit_transform(X)

    distance_matrix = pairwise_distances(X, metric='cosine')

    agglo = AgglomerativeClustering(n_clusters=n_clusters, metric='cosine', linkage='average')
    df["cluster"] = agglo.fit_predict(X)

    return df, X, distance_matrix

def get_Clusters(df, n_clusters = None, mode = 'KMEANS'):
    X = df.drop(["GEO", "PMID"], axis=1, inplace=False)
    if mode == 'KMEANS':
        if n_clusters is None: raise AttributeError
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, max_iter=500, init='k-means++')
        kmeans.fit(X)
        df['cluster'] = kmeans.labels_
    elif mode == 'Agglomerative':
        if n_clusters is None: raise AttributeError
        agglo = AgglomerativeClustering(n_clusters=n_clusters, linkage='average')
        agglo.fit(X)
        df['cluster'] = agglo.labels_
    return df, X



