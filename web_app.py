import mpld3
from flask import Flask, render_template, url_for, request, jsonify
import python_func.plotting as p_plot
import python_func.data_scrape as p_scrape
import python_func.clustering as p_cluster
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')
@app.route("/plot", methods=["POST"])
def plot():
    data = request.get_json('numbers', [])
    if not data:
        return jsonify("No data"), 400
    try:
        PMIDlist = list(map(int, data))
        PMID_GEOdict = p_scrape.getPMIDdict(PMIDlist)
        all_GEOS = p_scrape.getGEO(PMIDlist)
        data = p_scrape.geoToDf(all_GEOS, PMID_GEOdict)
        data = p_cluster.vectorize(data)
        data_fin, X, distance_matrix = p_cluster.get_Clusters2(data, 5)
        plot_html = p_plot.plotClusters(data_fin, X,distance_matrix)
        return jsonify({'plot': plot_html})



    except:
        return jsonify("Input should be PMID numbers separated by commas or newline"), 400

if __name__ == "__main__":
    app.run(debug=True)
