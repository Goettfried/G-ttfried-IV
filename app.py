from flask import Flask, render_template, request, redirect, url_for, session
from flask_httpauth import HTTPBasicAuth
import os
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

auth = HTTPBasicAuth()

users = {
    os.environ['USERNAME']: generate_password_hash(os.environ['PASSWORD'])
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
            session['logged_in'] = True
            return redirect(url_for('protected'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/protected')
@auth.login_required
def protected():
    return '''
        Logged in successfully<br>
        <a href="/logout">Logout</a>
    '''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
