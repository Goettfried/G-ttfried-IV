from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import pandas as pd
import io
import xlsxwriter

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://oesterreich:T48R0JhMHfLRQj3i86Tv3810txboBkOI@dpg-cqmn0so8fa8c73afbo0g-a:5432/bayern'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    message = db.Column(db.String(200), nullable=False)
    submission_type = db.Column(db.String(50), nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/')
def index():
    if 'loggedin' in session:
        form_data = FormData.query.order_by(FormData.submission_date.desc()).all()
        return render_template('index.html', form_data=form_data)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['loggedin'] = True
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    return redirect(url_for('login'))

@app.route('/receive_form', methods=['POST'])
def receive_form():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')
    submission_type = data.get('form_type')  # Assurez-vous que ce champ est bien envoyé

    if not submission_type:
        return jsonify({'error': 'Type de soumission inconnu'}), 400

    form_data = FormData(
        name=name,
        email=email,
        phone=phone,
        message=message,
        submission_type=submission_type,
        submission_date=datetime.utcnow()
    )
    db.session.add(form_data)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Soumission réussie'}), 200

@app.route('/export_data')
def export_data():
    form_data = FormData.query.all()
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Write headers
    worksheet.write('A1', 'Nom')
    worksheet.write('B1', 'Email')
    worksheet.write('C1', 'Numéro de téléphone')
    worksheet.write('D1', 'Message')
    worksheet.write('E1', 'Type de soumission')
    worksheet.write('F1', 'Date de soumission')

    # Write data
    row = 1
    for data in form_data:
        worksheet.write(row, 0, data.name)
        worksheet.write(row, 1, data.email)
        worksheet.write(row, 2, data.phone)
        worksheet.write(row, 3, data.message)
        worksheet.write(row, 4, data.submission_type)
        worksheet.write(row, 5, data.submission_date.strftime('%Y-%m-%d %H:%M:%S'))
        row += 1

    workbook.close()
    output.seek(0)

    return send_file(output, download_name='form_data.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)