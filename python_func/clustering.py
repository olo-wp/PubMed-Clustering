from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
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

    distance_matrix = pairwise_distances(X, metric='euclidean')

    kmeans = AgglomerativeClustering(n_clusters=n_clusters, metric='euclidean', linkage='ward')
    df["cluster"] = kmeans.fit_predict(distance_matrix)

    return df, X, distance_matrix
