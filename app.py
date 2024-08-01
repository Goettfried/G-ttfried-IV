from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
import pandas as pd
import openpyxl

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    db.init_app(app)
    return app

app = create_app()

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    message = db.Column(db.Text)
    type = db.Column(db.String(50))  # "Je recherche du travail" ou "Je recherche du personnel"

@app.route('/')
def index():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()
    return render_template('index.html', travail_data=travail_data, personnel_data=personnel_data)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')
    form_type = data.get('type')

    if not name or not email or not phone or not message or not form_type:
        return jsonify({"status": "error", "message": "Tous les champs sont obligatoires."}), 400

    form_data = FormData(name=name, email=email, phone=phone, message=message, type=form_type)
    db.session.add(form_data)
    db.session.commit()
    return jsonify({"status": "success", "message": "Données soumises avec succès."})

@app.route('/export_data', methods=['GET'])
def export_data():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()

    travail_df = pd.DataFrame([(d.name, d.email, d.phone, d.message) for d in travail_data],
                              columns=["Nom", "Email", "Numéro de téléphone", "Message"])
    personnel_df = pd.DataFrame([(d.name, d.email, d.phone, d.message) for d in personnel_data],
                                columns=["Nom", "Email", "Numéro de téléphone", "Message"])

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        travail_df.to_excel(writer, index=False, sheet_name='Travail')
        personnel_df.to_excel(writer, index=False, sheet_name='Personnel')

    output.seek(0)
    return send_file(output, attachment_filename="data.xlsx", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

