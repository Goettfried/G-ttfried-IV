from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
import os
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

auth = HTTPBasicAuth()

users = {
    os.environ['USERNAME']: os.environ['PASSWORD']
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_password(username, password):
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
