from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd
from io import BytesIO

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    message = db.Column(db.Text)

db.create_all()

@app.route('/')
def index():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()
    return render_template('index.html', travail_data=travail_data, personnel_data=personnel_data)

@app.route('/receive_form', methods=['POST'])
def receive_form():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400
    
    new_data = FormData(
        type=data.get('type'),
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        message=data.get('message')
    )
    
    db.session.add(new_data)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "Data received"}), 200

@app.route('/export_data')
def export_data():
    try:
        travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
        personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()

        travail_df = pd.DataFrame([{
            'Name': d.name,
            'Email': d.email,
            'Phone': d.phone,
            'Message': d.message
        } for d in travail_data])

        personnel_df = pd.DataFrame([{
            'Name': d.name,
            'Email': d.email,
            'Phone': d.phone,
            'Message': d.message
        } for d in personnel_data])

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='openpyxl')
        
        travail_df.to_excel(writer, sheet_name='Travail', index=False)
        personnel_df.to_excel(writer, sheet_name='Personnel', index=False)
        
        writer.save()
        output.seek(0)

        return send_file(output, attachment_filename="form_data.xlsx", as_attachment=True)
    except Exception as e:
        print(f"Error during export: {e}")
        return jsonify({"status": "error", "message": "Error during export"}), 500

if __name__ == '__main__':
    app.run(debug=True)
