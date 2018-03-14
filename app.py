import pandas as pd
from flask import Flask, render_template, jsonify

df = pd.read_csv('DataSets/belly_button_biodiversity_samples.csv')
otudf = pd.read_csv('DataSets/belly_button_biodiversity_otu_id.csv')

app = Flask(__name__)

@app.route("/")
def home():
    """Render Home Page."""
    return render_template("index.html")

@app.route("/samples/<sample>")
def samples(sample):

    x = otudf['otu_id'].values.tolist()
    y = df[sample].values.tolist()
    text = otudf['lowest_taxonomic_unit_found'].values.tolist()

    tempdf = pd.DataFrame({'a': y, 'b': x, 'c': text})
    selecttempdf = tempdf.nlargest(10, 'a')

    values = selecttempdf["a"].values.tolist()
    labels = selecttempdf["b"].values.tolist()
    hovertext = selecttempdf["c"].values.tolist()

    piedata = {"labels": labels, "values": values, "hovertext": hovertext, "type": "pie"}

    return jsonify(piedata)

@app.route("/samples/<sample>/otu")
def samplesotu(sample):

    x = otudf['otu_id'].values.tolist()
    y = df[sample].values.tolist()
    text = otudf['lowest_taxonomic_unit_found'].values.tolist()

    tempdf = pd.DataFrame({'a': y, 'b': x, 'c': text})
    selecttempdf = tempdf.dropna()

    newx = selecttempdf['b'].values.tolist()
    newy = selecttempdf['a'].values.tolist()
    newtext = selecttempdf['c'].values.tolist()

    bubbledata = {"x": newx, "y": newy, "hovertext": newtext, "mode": "markers", "marker": {"size": newy}}

    return jsonify(bubbledata)

if __name__ == '__main__':
    app.run(debug=True)