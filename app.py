from flask import *
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/tables")
def show_tables():
    data = pd.read_csv('MOCK_DATA.csv')
    s = pd.Series([0, 1])
    ax = s.plot.hist()
    ax.figure.savefig('static\demo-file.png')

    return render_template('view.html',tables=[data.to_html(classes='male')],
    titles = ['na'])

if __name__ == "__main__":
    app.run(debug=True)
    # https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html
    # https://dash.plotly.com/