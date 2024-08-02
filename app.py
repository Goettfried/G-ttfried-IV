from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import io
import os

app = Flask(__name__)
CORS(app)

# Configuration de la base de données
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'instance', 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'bf55b6617cb416f62fb5c63c6b874cfd')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

auth = HTTPBasicAuth()

users = {
    "Nicolas": generate_password_hash("Goetzinger")
}

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
def index():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()
    return render_template('index.html', travail_data=travail_data, personnel_data=personnel_data)

@app.route('/check_tables')
def check_tables():
    from sqlalchemy import inspect
    tables = inspect(db.engine).get_table_names()
    return f"Tables: {tables}"

@app.route('/init_db')
def init_db():
    db.create_all()
    return "Database initialized!"

@app.route('/export_data')
@auth.login_required
def export_data():
    output = io.BytesIO()
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()
    
    if not travail_data and not personnel_data:
        return "No data to export", 200
    
    df_travail = pd.DataFrame([(d.name, d.email, d.phone, d.message) for d in travail_data],
                              columns=["Name", "Email", "Phone", "Message"]) if travail_data else pd.DataFrame()
    df_personnel = pd.DataFrame([(d.name, d.email, d.phone, d.message) for d in personnel_data],
                                columns=["Name", "Email", "Phone", "Message"]) if personnel_data else pd.DataFrame()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        if not df_travail.empty:
            df_travail.to_excel(writer, sheet_name='Travail', index=False)
        if not df_personnel.empty:
            df_personnel.to_excel(writer, sheet_name='Personnel', index=False)
    
    output.seek(0)
    return send_file(output, download_name="data_export.xlsx", as_attachment=True)

@app.route('/receive_form', methods=['POST'])
def receive_form():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')  # Optional
    message = data.get('message')
    form_type = data.get('type')
    
    if not all([name, email, message, form_type]):
        return jsonify({"status": "error", "message": "Name, Email, Message and Type are required fields"}), 400

    form_data = FormData(name=name, email=email, phone=phone, message=message, type=form_type)
    db.session.add(form_data)
    db.session.commit()

    return jsonify({"status": "success", "message": "Form data received successfully"})

@app.route('/protected')
@auth.login_required
def protected():
    return render_template('protected.html')

@app.route('/logout')
@auth.login_required
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
