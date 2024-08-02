from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

auth = HTTPBasicAuth()

# Utilisateurs simulés
users = {
    "Nicolas": generate_password_hash(os.environ.get('PASSWORD', 'default_password'))
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_password(username, password):
            session['username'] = username
            return redirect(url_for('protected'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/protected')
@auth.login_required
def protected():
    return render_template('protected.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
