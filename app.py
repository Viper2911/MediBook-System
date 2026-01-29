from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
import os
import joblib
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

app=Flask(__name__)
app.config['SECRET_KEY']='medibook-secret-key-2026' 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

print("Loading ML Models")
tfidf=joblib.load('tfidf_vectorizer.pkl')
tfidf_matrix=joblib.load('tfidf_matrix.pkl')
doctors_df=joblib.load('doctors_df.pkl')
print("ML Models loaded successfully")

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=true)
    username=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    role=db.Column(db.String(50))
    
    specialist=db.Column(db.String(100),nullable=True)
    tags=db.Column(db.String(500),nullable=True)

class Appointment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    patient_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    doctor_name=db.Column(db.String(100))
    specialist=db.Column(db.String(100))
    date=db.Column(db.String(50))
    status=db.Column(db.String(50), default='Confirmed')
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))