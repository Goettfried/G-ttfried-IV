from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50))
    message = db.Column(db.Text, nullable=False)
    form_type = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session['username'] = user.username
            return redirect(url_for('index'))
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/protected')
def protected():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('protected.html', username=session['username'])

@app.route('/receive_form', methods=['POST'])
def receive_form():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')
    form_type = data.get('form_type')

    if not name or not email or not message or not form_type:
        return jsonify({'status': 'fail', 'message': 'Missing data'}), 400

    form_data = FormData(name=name, email=email, phone=phone, message=message, form_type=form_type)
    db.session.add(form_data)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Form data received'}), 200

@app.route('/view_data')
def view_data():
    if 'username' not in session:
        return redirect(url_for('login'))
    form_data = FormData.query.all()
    return render_template('view_data.html', form_data=form_data)

@app.route('/export_data')
def export_data():
    if 'username' not in session:
        return redirect(url_for('login'))
    form_data = FormData.query.all()
    data = [{'name': d.name, 'email': d.email, 'phone': d.phone, 'message': d.message, 'form_type': d.form_type} for d in form_data]
    df = pd.DataFrame(data)
    df.to_excel('form_data.xlsx', index=False)
    return jsonify({'status': 'success', 'message': 'Data exported to form_data.xlsx'})

if __name__ == '__main__':
    app.run(debug=True)

