from flask import Flask, render_template, request, redirect, url_for, session
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

auth = HTTPBasicAuth()

users = {
    os.getenv("USERNAME"): os.getenv("PASSWORD")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('protected'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.verify_password(username, password):
            session['username'] = username
            return redirect(url_for('protected'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/protected')
@auth.login_required
def protected():
    return 'Logged in successfully'

if __name__ == '__main__':
    app.run(debug=True)
