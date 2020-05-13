from flask import *
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
data=None
app = Flask(__name__)


@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file'] 
        global data
        data= pd.read_csv(f)
        head= data.head()
        return render_template("success.html", name = f.filename,head=head)  

@app.route("/tables")
def show_tables():
    return render_template('view.html',tables=[data.to_html(classes = '" id = "table')],
    titles = ['titol'])
@app.route("/graphics")
def show_graphics():
    
    ax = data.plot(kind='bar')
    ax.figure.savefig('static\demo-file.png')
    return render_template('graphic.html')

@app.route("/")
def index():
    return render_template('index.html')
@app.route('/upload')  
def upload():  
    return render_template("file_upload_form.html")  
 

if __name__ == "__main__":
    app.run(debug=True)
    # https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html
    