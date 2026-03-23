from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import joblib
import pandas as pd
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'medibook-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

tfidf = joblib.load('tfidf_vectorizer.pkl')
tfidf_matrix = joblib.load('tfidf_matrix.pkl')
doctors_df = joblib.load('doctors_df.pkl')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(50))
    specialist = db.Column(db.String(100), nullable=True)
    tags = db.Column(db.String(500), nullable=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_name = db.Column(db.String(100))
    specialist = db.Column(db.String(100))
    date = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Confirmed')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'Patient')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, role=role)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your username and password.')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    recommended_doctors = []
    
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        
        if symptoms:
            user_vector = tfidf.transform([symptoms])
            similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()
            top_indices = similarity_scores.argsort()[-5:][::-1]
            
            for idx in top_indices:
                score = round(similarity_scores[idx] * 100, 2)
                
                if score > 0:
                    doc_info = doctors_df.iloc[idx].to_dict()
                    doc_info['match_score'] = score
                    recommended_doctors.append(doc_info)
                    
            if not recommended_doctors:
                flash("We couldn't find a strong match for those symptoms. Please try describing them differently.")

    return render_template('search.html', doctors=recommended_doctors)

if __name__ == '__main__':
    app.run(debug=True)
