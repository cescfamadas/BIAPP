from flask import *
import pandas as pd
import matplotlib
import constants
matplotlib.use('Agg')
import matplotlib.pyplot as plt
data=None
app = Flask(__name__)

def generateDF():
    global data
    data= pd.read_csv('data.csv')  

@app.route("/info")
def getInfo():
    head= data.head()
    columns=list(data.columns)
    return render_template("info.html",head=head,columns=columns) 

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
@app.route('/upload')  
def upload():  
    return render_template("file_upload_form.html")  
 #endregion

if __name__ == "__main__":
    generateDF()
    app.run(debug=True)
    # https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html
    # https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    #https://queirozf.com/entries/pandas-dataframe-plot-examples-with-matplotlib-pyplot