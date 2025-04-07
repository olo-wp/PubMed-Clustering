# PubMed Clustering

---

This divides PubMed articles into clusters based on the GEO-database available experiments, that were used in a given article.

### How to use ?

The app is very easy to use. Install requirements listed in requirements.txt
with: 
```
pip install -r requirements.txt
```
then run
```
python3 web_app.py
```

In the console you will see a link for the web page, most probably http://127.0.0.1:5000
. All you have to do now is input PMID numbers of the articles you are interested in, choose clustering method, number of clusters and reduction method. From my observations the best ones were KMEANS with UMAP. After a while (10 - 30) seconds results will appear. Remember: You can move the plot and hover over points to get more info.