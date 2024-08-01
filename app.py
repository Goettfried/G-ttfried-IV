from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
from io import BytesIO
from auth import auth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if auth.verify_password(username, password):
            return redirect(url_for('index'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/index')
@auth.login_required
def index():
    return render_template('index.html')

@app.route('/receive_form', methods=['POST'])
def receive_form():
    data = request.get_json()
    if data.get('type') == 'Je-recherche-du-travail':
        save_data('travail', data)
    elif data.get('type') == 'Je-recherche-du-personnel':
        save_data('personnel', data)
    return {"status": "success", "message": "Form data received successfully"}

def save_data(category, data):
    # Logique pour sauvegarder les données dans la base de données ou fichier Excel
    pass

@app.route('/export_data')
@auth.login_required
def export_data():
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # Charger les données depuis la base de données ou les fichiers
    travail_df = pd.DataFrame()  # Remplacez par le chargement réel des données
    personnel_df = pd.DataFrame()  # Remplacez par le chargement réel des données

    travail_df.to_excel(writer, sheet_name='Travail', index=False)
    personnel_df.to_excel(writer, sheet_name='Personnel', index=False)

    writer.save()
    output.seek(0)

    return send_file(output, attachment_filename="data_export.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
