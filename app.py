from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance/app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
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
    return jsonify(tables)

@app.route('/export_data')
def export_data():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()

    if not travail_data and not personnel_data:
        return "No data to export"

    import pandas as pd
    from io import BytesIO
    from flask import send_file

    df_travail = pd.DataFrame([(d.name, d.email, d.phone, d.message) for d in travail_data],
                              columns=["Name", "Email", "Phone", "Message"])
    df_personnel = pd.DataFrame([(d.name, d.email, d.phone, d.message) for d in personnel_data],
                                columns=["Name", "Email", "Phone", "Message"])

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_travail.to_excel(writer, sheet_name='Travail', index=False)
        df_personnel.to_excel(writer, sheet_name='Personnel', index=False)
    output.seek(0)

    return send_file(output, download_name="data_export.xlsx", as_attachment=True)

@app.route('/receive_form', methods=['POST'])
def receive_form():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')
    type = data.get('type')

    if not all([name, email, phone, message, type]):
        return jsonify({"status": "error", "message": "Missing data fields"}), 400

    new_entry = FormData(name=name, email=email, phone=phone, message=message, type=type)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"status": "success", "message": "Form data received successfully"})

if __name__ == '__main__':
    app.run(debug=True)

