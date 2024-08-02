from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import os
import io
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# Create the database model
class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    type = db.Column(db.String(50))

# Home route
@app.route('/')
def index():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()
    return render_template('protected.html', travail_data=travail_data, personnel_data=personnel_data)

# Export data route
@app.route('/export_data')
def export_data():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    personnel_data = FormData.query.filter_by(type="Je recherche du personnel").all()

    travail_df = pd.DataFrame([(d.id, d.name, d.email, d.type) for d in travail_data], columns=['ID', 'Name', 'Email', 'Type'])
    personnel_df = pd.DataFrame([(d.id, d.name, d.email, d.type) for d in personnel_data], columns=['ID', 'Name', 'Email', 'Type'])

    with pd.ExcelWriter('exported_data.xlsx') as writer:
        travail_df.to_excel(writer, sheet_name='Travail', index=False)
        personnel_df.to_excel(writer, sheet_name='Personnel', index=False)

    return send_file('exported_data.xlsx', as_attachment=True)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.verify_password(username, password):
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

# Protected route
@app.route('/protected')
@auth.login_required
def protected():
    return render_template('protected.html')

# Logout route
@app.route('/logout')
def logout():
    return redirect(url_for('login'))

# Verify password
@auth.verify_password
def verify_password(username, password):
    return username == os.getenv('ADMIN_USERNAME') and password == os.getenv('ADMIN_PASSWORD')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
