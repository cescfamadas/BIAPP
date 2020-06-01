import os
from flask import *
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
data=None
app = Flask(__name__)

def generateDF():
    global data
    mode = os.getenv("MODE")
    if mode == "prod":
        data= pd.read_csv('/app/data.csv')
    else:
        data= pd.read_csv('data.csv')

@app.route("/info")
def getInfo():
    head= data.head()
    columns=list(data.columns)
    return render_template("info.html",head=head,columns=columns) 

@app.route("/data.csv")
def getFile():
    mode = os.getenv("MODE")
    if mode == "prod":
        return app.send_static_file('/app/data.csv')
    else:
        return app.send_static_file('data.csv')


#region<success>
""" # @app.route('/success', methods = ['POST'])  
# def success():  
#     if request.method == 'POST':  
#         f = request.files['file'] 
#         global data
#         data= pd.read_csv(f)
#         head= data.head()
#         columns=list(data.columns) 
#         return render_template("success.html", name = f.filename,head=head,columns=columns)   """
#endregion
@app.route("/tables")
def show_tables():
    return render_template('view.html',tables=[data.to_html(classes = '" id = "table')],
    titles = ['titol'])

@app.route("/graphics")
def show_graphics():
   data.groupby(['country','profession']).size().unstack().plot(kind='bar',stacked=True)
   plt.savefig('static\demo-file.png')
   return render_template('graphic.html')

@app.route("/")
def index():
    return render_template('index.html')

#region<upload>
# @app.route('/upload')  
# def upload():  
#     return render_template("file_upload_form.html")  
 #endregion

if __name__ == "__main__":
    generateDF()
    mode = os.getenv("MODE")
    if mode == "prod":
        app.run(debug=True)
    else:
        app.run(debug=True)
    # https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html
    # https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    #https://queirozf.com/entries/pandas-dataframe-plot-examples-with-matplotlib-pyplot