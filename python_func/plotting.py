import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

    colors = px.colors.qualitative.Plotly
    last_col = max(df["cluster"]) + 1
    color_map = {i: colors[i % len(colors)] for i in range(last_col)}
    df["col"] = df["cluster"].map(color_map)

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.7, 0.3],
        subplot_titles=["Cluster visualization","PMIDS by Cluster"],
        specs=[[{"type":"xy"},{"type":"table"}]]
    )

    Cluster_PMID = dict()
    for cluster in sorted(df["cluster"].unique()):
        cluster_data = df[df["cluster"] == cluster]
        print(f"Cluster {cluster} data:\n", cluster_data[["x-axis", "y-axis"]].head())

        C_PMID = frozenset(cluster_data["PMID"])
        Cluster_PMID[cluster] = C_PMID

        fig.add_trace(
            go.Scatter(
                x=list(cluster_data["x-axis"]),
                y=list(cluster_data["y-axis"]),
                mode='markers',
                marker=dict(color=color_map[cluster], size=10, opacity=0.8, symbol='square'),
                name=f"Cluster {cluster + 1}",
                text = [f"PMID: {pmid} GEO: {geo}" for pmid, geo in zip(cluster_data["PMID"], cluster_data["GEO"])],
                hoverinfo='text+x+y'
            ),
            row=1, col=1
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
            ),
            row=1,col=1
        )

    table_header = ["Cluster", "PMIDs"]
    table_data = [[f"Cluster {cluster + 1}", ", ".join(map(str, pmids))] for cluster, pmids in Cluster_PMID.items()]

    fig.add_trace(
        go.Table(
            header=dict(values=table_header, fill_color='lightgrey', align='left'),
            cells=dict(values=list(zip(*table_data)), align='left')
        ),
        row=1, col=2
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