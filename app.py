from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# Utilisateurs simulés
users = {
    "Nicolas": generate_password_hash(os.environ.get('PASSWORD', 'default_password'))
}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            flash('Connexion réussie.', 'success')
            return redirect(url_for('protected'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
    return render_template('login.html')

@app.route('/protected')
def protected():
    if 'username' in session:
        return render_template('protected.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Déconnexion réussie.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
