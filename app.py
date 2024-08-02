from flask import Flask, render_template, request, redirect, url_for, session
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'bf55b6617cb416f62fb5c63c6b874cfd'

auth = HTTPBasicAuth()

users = {
    "Nicolas": generate_password_hash('Goetzinger')
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.verify_password(username, password):
            session['username'] = username
            return redirect(url_for('protected'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/protected')
@auth.login_required
def protected():
    if 'username' in session:
        return '''
        <h1>Logged in successfully</h1>
        <a href="{{ url_for('logout') }}">Se déconnecter</a>
        '''
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
