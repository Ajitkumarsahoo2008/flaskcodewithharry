from flask import Flask,render_template,request



#from database.db import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pymysql
import sys
import json

with open("config.json","r") as c:
   params = json.load(c)["params"]
local_server = True
app=Flask(__name__)
#conn=pymysql.connect(db='ajit', user='malli',password='Rama@1234',host='localhost', port=3306)
#print(conn)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://malli:Rama@1234@localhost/ajit'
#sys.exit()
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
    
#app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String(100))
    date  = db.Column(db.DateTime,nullable = False,default = datetime.utcnow)


class contacts(db.Model):
    __tablename__ = "contacts"
    sno = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(30))
    phone_num = db.Column(db.Integer())
    mes  = db.Column(db.String(500))
    date = db.Column(db.DateTime,nullable=False,default = datetime.utcnow)

db.create_all() # In case user table doesn't exists already. Else remove it.  
#db.session.add(admin)

#db.session.commit() # This is needed to write the changes to database



@app.route("/blog")
def bootstrap():
    return render_template('blogfile.html',params=params)

@app.route("/index")
def index():
    return render_template('index.html',params=params)

@app.route("/about")
def about():
    return render_template('about.html',params=params)

@app.route("/contact",methods=['GET','POST'])
def contact():
    if (request.method=='post'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone_no = request.form.get('phone_no')
        message = request.form.get('message')
    
        entry=contacts(name=name,phone_no=phone_no,date=datetime.now(),message=message,email=email)
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html',params=params)


if  __name__=="__main__":
    app.run(port=5002,debug=True)


