from os import name
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import  SQLAlchemy
from marks import calculate
import pickle
import numpy as np

with open ('personality_prediction_lr', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Applicants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Applicants(db.Model):
    app_id = db.Column(db.String(100), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    gender = db.Column(db.String(10), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    o = db.Column(db.Integer, nullable = False)
    n = db.Column(db.Integer, nullable = False)
    c = db.Column(db.Integer, nullable = False)
    a = db.Column(db.Integer, nullable = False)
    e = db.Column(db.Integer, nullable = False)
    Personality = db.Column(db.String(20), nullable = False)

    def __repr__(self) -> str:
        return f"{self.app_id}-{self.name} - {self.gender} - {self.age} - {self.o} - {self.n} - {self.c} - {self.a} - {self.e} - {self.Personality}"
    def __init__(self, app_id, name, gender, age, o, n, c, a, e, Personality):
        self.app_id = app_id
        self.name = name
        self.gender = gender
        self.age = age
        self.o = o
        self.n = n
        self.c = c
        self.a = a
        self.e = e
        self.Personality = Personality
        
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        app_id = request.form['id1']
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        detail = app_id + "-" + name + "-" + gender + "-" + age
        return redirect(url_for("quiz", details = detail))
    return render_template("register.html")
    
@app.route('/quiz/<details>', methods = ['GET', 'POST'])
def quiz(details):
    if request.method == 'POST':
        ans = []
        ans.append(request.form.getlist('mycheckbox')[0])
        ans.append(request.form.getlist('mycheckbox1')[0])
        ans.append(request.form.getlist('mycheckbox2')[0])
        ans.append(request.form.getlist('mycheckbox3')[0])
        ans.append(request.form.getlist('mycheckbox4')[0])
        ans.append(request.form.getlist('mycheckbox5')[0])
        ans.append(request.form.getlist('mycheckbox6')[0])
        ans.append(request.form.getlist('mycheckbox7')[0])
        ans.append(request.form.getlist('mycheckbox8')[0])
        ans.append(request.form.getlist('mycheckbox9')[0])
        essentials = details.split('-')
        o1, c1, e1, a1, n1 = calculate(ans)
        data = []
        if(essentials[2].lower()=='male'):
            data.append(1)
        else:
            data.append(0)
        data.append(int(essentials[3]))
        data.append(o1)
        data.append(n1)
        data.append(c1)
        data.append(a1)
        data.append(e1)
        data = np.array(data).reshape(1,7)
        p = model.predict(data)
        apply = Applicants(app_id = essentials[0], name = essentials[1], gender = essentials[2], age = int(essentials[3]),o = o1,n= n1,c= c1,a= a1,e = e1, Personality = p[0])
        db.session.add(apply)
        db.session.commit()
        return redirect(url_for("submit"))
    return render_template("quiz.html")

@app.route('/submit')
def submit():
    return render_template("submit.html")

@app.route('/recruiter-login', methods = ['GET', 'POST'])
def recruiter():
    if request.method == 'POST':
        return render_template("recruiter.html")
    return render_template("recruiter.html")

@app.route('/data')
def data():
    apply = Applicants.query.all()
    return render_template("data.html", applicants = apply)

if __name__=="__main__":
    app.run(debug = True, port = 4000)