from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pandas as pd
from io import BytesIO
from auth import auth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.verify_password(username, password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()
    return render_template('index.html', travail_data=travail_data, personnel_data=personnel_data)

@app.route('/receive_form', methods=['POST'])
def receive_form():
    data = request.get_json()
    new_entry = FormData(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone', ''),
        message=data['message'],
        type=data['type']
    )
    db.session.add(new_entry)
    db.session.commit()
    return {"status": "success", "message": "Form data received successfully"}

@app.route('/export_data')
@login_required
def export_data():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()

    travail_df = pd.DataFrame([(d.name, d.email, d.phone, d.message) for d in travail_data], columns=["Name", "Email", "Phone", "Message"])
    personnel_df = pd.DataFrame([(d.name, d.email, d.phone, d.message) for d in personnel_data], columns=["Name", "Email", "Phone", "Message"])

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    travail_df.to_excel(writer, sheet_name='Travail', index=False)
    personnel_df.to_excel(writer, sheet_name='Personnel', index=False)
    writer.save()
    output.seek(0)

    return send_file(output, attachment_filename="data_export.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
