import os
import pathlib
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pandas as pd
import matplotlib
import sqlite3
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import logging
import DFToSql
from flask import jsonify


data=None
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
db_url=app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(200),nullable=False)
    country=db.Column(db.String(200),nullable=False)
    city=db.Column(db.String(200),nullable=False)
    profession=db.Column(db.String(200),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    gender=db.Column(db.String(50),nullable=False)
    rand=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return '<User id={} first name={} country={} city={} profession={} age={} gender={} rand={}>'.format(self.id,self.firstname,self.country,self.city,self.profession,self.age,self.gender,self.rand)


def generateDF():
    global data
    engine = create_engine(db_url)
    sqlite_connection = engine.connect()
    sqlite_table = "User"
    data=pd.read_sql(sqlite_table, sqlite_connection)
    data.drop(['index'],axis=1)
    sqlite_connection.close()

@app.route("/regenerateDF")
def regenerateDF():
    generateDF()
    return redirect('/')

@app.route("/getuser/<id>")
def getUserById(id):
    user=User.query.get(id)
    return render_template("user.html",user=user)
@app.route("/getusers")
def getUsers():
    users=User.query.all()
    return render_template("user.html",user=users)

@app.route("/adduser")
def addUserForm():
    return render_template("addUserForm.html")
@app.route("/info")
def getInfo():
    head= data.head()
    columns=list(data.columns)
    return render_template("info.html",head=head,columns=columns) 

@app.route("/add",methods=['POST'])
def adduser():
    if request.method== 'POST':
        logging.info("POST")
        user_id=request.form['id']
        user_firstname=request.form['firstname']
        user_country=request.form['country']
        user_profession=request.form['profession']
        user_age=request.form['age']
        user_gender=request.form['gender']
        user_rand=request.form['rand']
        new_user=User(id=user_id,firstname=user_firstname,country=user_country,profession=user_profession,age=user_age,gender=user_gender,rand=user_rand)
        try:
            db.session.add(new_user)
            db.session.commit()
        except EnvironmentError:
            print("error al inserir usuari")
    return redirect("/")
@app.route("/json")
def dfToJson():
    # users=User.query.all()
    # return jsonify(users)
    return Response(data.to_json(orient="records"), mimetype='application/json')


@app.route("/hello/<name>")
@app.route("/hello",defaults={'name': 'john'})

def sayHello(name):
   return render_template("hello.html",name=name)


@app.route("/tables")
def show_tables():
    users=User.query.all()
    return render_template('view.html',users=users)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.route("/graphics")
def show_graphics():
   data.groupby(['country','profession']).size().unstack().plot(kind='bar',stacked=True)
   plt.savefig('static\demo-file.png')
   
   data.groupby(['gender','profession']).size().unstack().plot(kind='bar',stacked=True)
   plt.savefig('static\demo-file1.png')
   
   data[['age']].plot(kind='hist',bins=[18,22,26,30,35],rwidth=0.8)
   plt.savefig('static\demo-file2.png')
   
   data.plot(kind='scatter',x='rand',y='age')
   plt.savefig('static\demo-file3.png')
   
   return render_template('graphic.html')


@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    file = pathlib.Path("test.db")
    if file.exists():
        generateDF()
    else:
        DFToSql.dfToSql()
        generateDF()
    app.register_error_handler(404, not_found)
    app.run(debug=True)
    # https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html
    # https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    #https://queirozf.com/entries/pandas-dataframe-plot-examples-with-matplotlib-pyplot