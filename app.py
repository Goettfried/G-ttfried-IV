import os
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/receive_form', methods=['POST'])
def receive_form():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')

    # Logique pour traiter les données et envoyer un email
    print(f"Received data: {name}, {email}, {phone}, {message}")

    # Envoyer un email avec les données reçues
    send_email(name, email, phone, message)

    return jsonify({'status': 'success', 'message': 'Form data received'}), 200

def send_email(name, email, phone, message):
    sender_email = os.getenv('EMAIL_USER')
    receiver_email = "destinataire@example.com"
    password = os.getenv('EMAIL_PASS')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Nouveau message de contact"

    body = f"Nom: {name}\nEmail: {email}\nTéléphone: {phone}\nMessage: {message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email envoyé avec succès")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")

if __name__ == '__main__':
    app.run(debug=True)