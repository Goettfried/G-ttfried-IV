from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas as pd
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()
    return render_template('index.html', travail_data=travail_data, personnel_data=personnel_data)

@app.route('/check_tables')
def check_tables():
    tables = db.engine.table_names()
    return f"Tables: {tables}"

@app.route('/init_db')
def init_db():
    db.create_all()
    return "Database initialized!"

@app.route('/export_data')
def export_data():
    output = io.BytesIO()
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()
    df_travail = pd.DataFrame([(d.name, d.email, d.phone, d.message) for d in travail_data],
                              columns=["Name", "Email", "Phone", "Message"])
    df_personnel = pd.DataFrame([(d.name, d.email, d.phone, d.message) for d in personnel_data],
                                columns=["Name", "Email", "Phone", "Message"])
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_travail.to_excel(writer, sheet_name='Travail', index=False)
        df_personnel.to_excel(writer, sheet_name='Personnel', index=False)
    output.seek(0)
    return send_file(output, download_name="data_export.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

