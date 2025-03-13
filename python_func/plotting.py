import plotly.express as px
import plotly.graph_objects as go
from sklearn.manifold import MDS
import pandas as pd
from flask import jsonify

def plotClusters(df, X, DD):
    mds = MDS(n_components=2, dissimilarity='euclidean')
    X_mds = mds.fit_transform(DD)
    df["MDS1"] = X_mds[:, 0]
    df["MDS2"] = X_mds[:, 1]

    colors = px.colors.qualitative.Plotly
    last_col = max(df["cluster"]) + 1
    color_map = {i: colors[i % len(colors)] for i in range(last_col)}
    df["col"] = df["cluster"].map(color_map)

    fig = go.Figure()

    for cluster in sorted(df["cluster"].unique()):
        cluster_data = df[df["cluster"] == cluster]
        fig.add_trace(
            go.Scatter(
                x=cluster_data["MDS1"],
                y=cluster_data["MDS2"],
                mode='markers',
                marker=dict(color=color_map[cluster], size=10, opacity=0.6),
                name=f"Cluster {cluster + 1}",
                text=[f"PMID: {pmid}" for pmid in cluster_data["PMID"]],  # Tooltip z PMID
                hoverinfo='text+x+y'
            )
        )

    centroids = df.groupby("cluster")[["MDS1", "MDS2"]].mean()
    for cluster in centroids.index:
        fig.add_trace(
            go.Scatter(
                x=[centroids.loc[cluster, "MDS1"]],
                y=[centroids.loc[cluster, "MDS2"]],
                mode='markers',
                marker=dict(color=color_map[cluster], size=15, symbol='triangle-up'),
                name=f"Centroid {cluster + 1}",
                hoverinfo='none'
            )
        )

    fig.update_layout(
        title="Cluster Visualization",
        xaxis_title="MDS1",
        yaxis_title="MDS2",
        template="plotly_dark",
        legend_title="Clusters",
        hovermode='closest'
    )

    try:
        plot_html = fig.to_html(full_html=False)
        return plot_html
    except Exception as e:
        print(e)
        return jsonify({"plot": "fail"})