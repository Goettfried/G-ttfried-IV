from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from auth import auth
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'bf55b6617cb416f62fb5c63c6b874cfd')  # Clé secrète ajoutée directement

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.authenticate(username, password):
            return redirect(url_for('protected'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/protected')
@auth.login_required
def protected():
    return 'Logged in successfully'

if __name__ == '__main__':
    app.run(debug=True)
