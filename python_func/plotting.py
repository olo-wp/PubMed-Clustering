import matplotlib.pyplot as plt
import matplotlib
import mplcursors as mpl
from matplotlib.lines import Line2D
from sklearn.manifold import MDS
import mpld3
from mpld3 import plugins
from data.colors import colors as c

def plotClusters(df, X, DD):
    colors = c

    last_col = max(df["cluster"]) + 1
    colors = colors[:last_col]

    color_map = {i: colors[i] for i in range(last_col)}
    df["col"] = df["cluster"].map(color_map)

    fig, ax = plt.subplots(figsize=(7, 7))

    plt.style.use('dark_background')


    mds = MDS(n_components=2, dissimilarity='euclidean')
    X_mds = mds.fit_transform(DD)

    df["MDS1"] = X_mds[:, 0]
    df["MDS2"] = X_mds[:, 1]


    """
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(DD)

    df["PCA1"] = X_pca[:, 0]
    df["PCA2"] = X_pca[:, 1]
    """

    scatter = ax.scatter(df["MDS1"], df["MDS2"], c=df["col"], alpha=0.6, s=40)

    labels = [f"PMID: {pmid}" for pmid in df["PMID"]]

    tooltip = plugins.PointLabelTooltip(scatter, labels=labels)
    plugins.connect(fig, tooltip)

    centroids = df.groupby("cluster")[["MDS1", "MDS2"]].mean()

    ax.scatter(centroids["MDS1"], centroids["MDS2"], marker='^', c=colors[:len(centroids)], s=30)

    scatter_plots = []
    labels_leg = []

    for cluster in sorted(df["cluster"].unique()):
        cluster_data = df[df["cluster"] == cluster]
        scatter = ax.scatter(cluster_data["MDS1"], cluster_data["MDS2"],
                             c=color_map[cluster], alpha=0.6, s=40)
        scatter_plots.append(scatter)
        labels_leg.append(f"Cluster {cluster+1}")

    legend = plugins.InteractiveLegendPlugin(scatter_plots, labels_leg, alpha_unsel=0.2, alpha_over=1.0)
    plugins.connect(fig, legend)

    ax.xlabel("PCA1")
    ax.ylabel("PCA2")
    ax.title("Cluster visualisation")

    return mpld3.fig_to_html(fig)
