import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA, TruncatedSVD
import pandas as pd
from flask import jsonify
from sklearn.manifold import TSNE
import umap


def plotClusters(df, X, dim_reduction = "PCA"):
    reduced = None
    if(dim_reduction == "PCA"):
        pca = PCA(n_components=2)
        reduced = pca.fit_transform(X)
    elif(dim_reduction == "TSNE"):
        tsne = TSNE(n_components=2)
        reduced = tsne.fit_transform(X)
    elif(dim_reduction == "SVD"):
        svd = TruncatedSVD(n_components=2)
        reduced = svd.fit_transform(X)
    elif(dim_reduction == "UMAP"):
        red = umap.UMAP(n_components=2, random_state=42, min_dist=0.2)
        reduced = red.fit_transform(X)

    df["x-axis"] = reduced[:, 0]
    df["y-axis"] = reduced[:, 1]

    """
    mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
    X_mds = mds.fit_transform(X)
    df["MDS1"] = X_mds[:, 0]
    df["MDS2"] = X_mds[:, 1]


    if df[["MDS1", "MDS2"]].isnull().any().any():
        print("Warning: NaN values found in MDS coordinates. Please check your input data.")
        return jsonify({"plot": "fail"})
    """
    colors = px.colors.qualitative.Plotly
    last_col = max(df["cluster"]) + 1
    color_map = {i: colors[i % len(colors)] for i in range(last_col)}
    df["col"] = df["cluster"].map(color_map)

    fig = go.Figure()

    for cluster in sorted(df["cluster"].unique()):
        cluster_data = df[df["cluster"] == cluster]
        print(f"Cluster {cluster} data:\n", cluster_data[["x-axis", "y-axis"]].head())

        fig.add_trace(
            go.Scatter(
                x=list(cluster_data["x-axis"]),
                y=list(cluster_data["y-axis"]),
                mode='markers',
                marker=dict(color=color_map[cluster], size=10, opacity=0.8, symbol='square'),
                name=f"Cluster {cluster + 1}",
                text=[f"PMID: {pmid}" for pmid in cluster_data["PMID"]],
                hoverinfo='text+x+y'
            )
        )

    centroids = df.groupby("cluster")[["x-axis", "y-axis"]].mean()
    for cluster in centroids.index:
        fig.add_trace(
            go.Scatter(
                x=[centroids.loc[cluster, "x-axis"]],
                y=[centroids.loc[cluster, "y-axis"]],
                mode='markers',
                marker=dict(color=color_map[cluster], size=15, symbol='triangle-up', opacity=1),
                name=f"Centroid {cluster + 1}",
                hoverinfo='none'
            )
        )

    fig.update_layout(
        title="Cluster Visualization",
        xaxis_title="x",
        yaxis_title="y",
        template="plotly_dark",
        legend_title="Clusters",
        hovermode='closest'
    )

    try:
        plot_html = fig.to_plotly_json()
        return plot_html
    except Exception as e:
        print(e)
        return jsonify({"plot": "fail"})