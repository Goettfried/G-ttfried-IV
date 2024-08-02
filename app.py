import os
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask("https://welshapp.onrender.com")
app.config['SECRET_KEY'] = 'votre_cle_secrete'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/41765/Desktop/Göttfried IV/instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Définissez vos modèles ici
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)

# Routes
@app.route('/')
def index():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()
    return render_template('protected.html', travail_data=travail_data, personnel_data=personnel_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/export_data')
def export_data():
    # Logique pour exporter les données
    return "Exportation des données"

if __name__ == '__main__':
    app.run()