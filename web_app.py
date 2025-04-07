from flask import Flask, render_template, url_for, request, jsonify
import python_func.plotting as p_plot
import python_func.data_scrape as p_scrape
import python_func.clustering as p_cluster
import plotly.express as px
import plotly.graph_objects as go
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/plot", methods=["POST"])
def plot():
    PMIDlist = request.get_json()
    print(type(PMIDlist['pmids']))
    print(PMIDlist['method'])
    print(PMIDlist)
    Clusters = int(PMIDlist['clusters'])
    Method = PMIDlist['method']
    Reduction = PMIDlist['reduction']
    PMIDlist = PMIDlist['pmids']
    if not PMIDlist:
        return jsonify("No data"), 400
    try:

        PMID_GEOdict = p_scrape.getPMIDdict(PMIDlist)
        all_GEOS = p_scrape.getGEO(PMIDlist)
        data = p_scrape.geoToDf(all_GEOS, PMID_GEOdict)
        data = p_cluster.vectorize(data)
        data_fin, X = p_cluster.get_Clusters(data,n_clusters=Clusters,mode=Method)
        plot_html = p_plot.plotClusters(data_fin, X, dim_reduction=Reduction)

        return plot_html
    except Exception as e:
        print(e)
        return jsonify("Input should be PMID numbers separated by commas or newline"), 400


if __name__ == "__main__":
    app.run(debug=True)
