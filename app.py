from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

users = {
    os.getenv("USERNAME"): os.getenv("PASSWORD")
}

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
        if username in users and check_password_hash(users.get(username), password):
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
def protected():
    if 'username' in session:
        return '''
            Logged in successfully
            <br><a href="{{ url_for('logout') }}">Se déconnecter</a>
        '''
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
