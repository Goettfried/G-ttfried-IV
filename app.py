from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Configurer SQLAlchemy avec une base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Définir le modèle de données
class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    message = db.Column(db.String(500))
    type = db.Column(db.String(50))

db.create_all()

# Route pour afficher les données des formulaires
@app.route('/')
def index():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()
    return render_template('index.html', travail_data=travail_data, personnel_data=personnel_data)

# Route pour recevoir les données du formulaire
@app.route('/receive_form', methods=['POST'])
def receive_form():
    data = request.get_json()
    if data:
        new_data = FormData(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            message=data.get('message'),
            type=data.get('type')
        )
        db.session.add(new_data)
        db.session.commit()
        return jsonify({"status": "success", "message": "Form data received"}), 200
    return jsonify({"status": "error", "message": "No data received"}), 400

# Route pour exporter les données en fichier Excel
@app.route('/export_data')
def export_data():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()

    travail_df = pd.DataFrame([(d.name, d.email, d.phone, d.message) for d in travail_data], columns=['Name', 'Email', 'Phone', 'Message'])
    personnel_df = pd.DataFrame([(d.name, d.email, d.phone, d.message) for d in personnel_data], columns=['Name', 'Email', 'Phone', 'Message'])

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')

    travail_df.to_excel(writer, sheet_name='Travail', index=False)
    personnel_df.to_excel(writer, sheet_name='Personnel', index=False)

    writer.save()
    output.seek(0)

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=form_data.xlsx'
    response.headers['Content-type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
