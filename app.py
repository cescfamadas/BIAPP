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
from werkzeug.exceptions import HTTPException
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io


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
        return 'User id={} first name={} country={} city={} profession={} age={} gender={} rand={}'.format(self.id,self.firstname,self.country,self.city,self.profession,self.age,self.gender,self.rand)


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
    return render_template("user.html",user=user, title="USER {}".format(user.id))

@app.route("/deleteuser/<id>")
def deleteUser(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/tables")

@app.route("/getusers")
def getUsers():
    users=User.query.all()
    return render_template("user.html",users=users,title="ALL USERS")
    
@app.route("/adduser")
def addUserForm():
    return render_template("addUserForm.html",title="ADD USER")
@app.route("/modifyUser/<id>",methods=['GET','POST'])
def modifyUser(id):
    user=User.query.get(id)
    if request.method== 'GET':
        return render_template("modifyUserForm.html",user=user,title=" MODIFY USER {}".format(user.id))
    elif request.method== 'POST':
        user.id=request.form['id']
        user.firstname=request.form['firstname']
        user.city=request.form['city']
        user.country=request.form['country']
        user.profession=request.form['profession']
        user.age=request.form['age']
        user.gender=request.form['gender']
        user.rand=request.form['rand']
        try:
            db.session.commit()
        except Exception:
            print(Exception)
    return redirect("/tables")


@app.route("/info")
def getInfo():
    head= data.head()
    columns=list(data.columns)
    count=data.count()
    return render_template("info.html",head=head,columns=columns,count=count,title="INFO") 

@app.route("/add",methods=['POST'])
def adduser():
    if request.method== 'POST':
        logging.info("POST")
        user_id=request.form['id']
        user_firstname=request.form['firstname']
        user_city=request.form['city']
        user_country=request.form['country']
        user_profession=request.form['profession']
        user_age=request.form['age']
        user_gender=request.form['gender']
        user_rand=request.form['rand']
        new_user=User(id=user_id,firstname=user_firstname,city=user_city,country=user_country,profession=user_profession,age=user_age,gender=user_gender,rand=user_rand)
        try:
            db.session.add(new_user)
            db.session.commit()
        except EnvironmentError:
            print("error al inserir usuari")
    return redirect("/")

@app.route("/json")
def dfToJson():
    return render_template("json.html",json=data.to_json(orient="records"),title="JSON")

@app.route('/plot',methods=['GET','POST'])
def plots():
    columns=list(data.columns)
    if request.method== 'GET':
        return render_template("plot.html",columns=columns)
    elif request.method=='POST':
        var1= request.form['var1']
        var2= request.form['var2']
        url="/plot/{}/{}".format(var1,var2)
        return render_template("plot.html",columns=columns,url=url)

@app.route('/plot/<var1>/<var2>')
def plot(var1,var2):
	pie =data.groupby([var1,var2]).size().unstack().plot(kind='bar',stacked=True)
	fig = pie.get_figure()
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response


@app.route("/hello/<name>")
@app.route("/hello",defaults={'name': 'john'})
def sayHello(name):
   return render_template("hello.html",name=name,title="HELLO {}".format(name))


@app.route("/tables")
def show_tables():
    users=User.query.all()
    return render_template('view.html',users=users,title="USERS TABLE")

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html',title="ERROR 404",e=e), 404

@app.errorhandler(500)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template("500_generic.html",title="ERROR 500", e=e), 500

@app.route("/graphics")
def show_graphics():
   names=[]
   data.groupby(['country','profession']).size().unstack().plot(kind='bar',stacked=True)
   plt.savefig('static\country-profession.png')
   names.append("country-profession")
   
   data.groupby(['gender','profession']).size().unstack().plot(kind='bar',stacked=True)
   plt.savefig('static\gender-profession')
   names.append("gender-profession")

   data[['age']].plot(kind='hist',bins=[18,22,26,30,35],rwidth=0.8)
   plt.savefig('static\hist-age.png')
   names.append("hist-age")
   
   data.plot(kind='scatter',x='rand',y='age')
   plt.savefig('static\scatter-rand-age.png')
   names.append("scatter-rand-age")
   
   return render_template('graphic.html',title="GRAPHICS",names=names)


@app.route("/")
def index():
    return render_template('index.html',title="HOME")


if __name__ == "__main__":
    file = pathlib.Path("test.db")
    if file.exists():
        generateDF()
    else:
        DFToSql.dfToSql()
        generateDF()
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, handle_exception)
    app.run()
