from flask import Flask, render_template, request,send_file,send_from_directory,redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
import os
from werkzeug import secure_filename
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/detail'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'gvsghjdsj'
db = SQLAlchemy(app)  

class Info(db.Model):
    name = db.Column(db.String(100))
    email = db.Column(db.String(100),primary_key=True)
    password = db.Column(db.String(100))

class Post(db.Model):
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    sid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    text = db.Column(db.String(1000))


@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method == 'POST'):
        email  = request.form['Email']
        password = request.form['Password']
        sig = Info.query.all()
        for i in sig:
            if i.email == email and i.password == password:
                session['Name']=i.name
                session['Email']=i.email
                return redirect(url_for('postbook'))
        return render_template('index.html',message='Not Registered')
    return render_template('index.html',message='')

@app.route('/logout')
def logout():
   session.pop('email',None)
   session.pop('name',None)
   return redirect('/')

@app.route('/register',methods=['GET','POST'])
def register():
    if(request.method == 'POST'):
        name = request.form['Name']
        email  = request.form['Email']
        password = request.form['Password']
        signature = Info(name=name,email=email,password=password)
        db.session.add(signature)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/postbook',methods=['GET','POST'])
def postbook():
    post1 = Post.query.all()
    if request.method == 'POST':
        text = request.form['text']
        signature = Post(name=session['Name'],email=session['Email'],text=text)
        db.session.add(signature)
        db.session.commit()
        post = Post.query.all()
        return render_template('postbook.html',post=post)
    return render_template('postbook.html',post=post1)

@app.route('/')
def main():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)