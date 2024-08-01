# This is a forced update to trigger redeployment

from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

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

    # Traitez et stockez les données comme nécessaire
    print(f"Received data: {name}, {email}, {phone}, {message}")

    try:
        send_email(name, email, phone, message)
        return jsonify({'status': 'success', 'message': 'Form data received'}), 200
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to send email'}), 500

def send_email(name, email, phone, message):
    sender_email = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASS']
    receiver_email = "votre.email@exemple.com"

    subject = "New Form Submission"
    body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

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
        raise

if __name__ == '__main__':
    app.run(debug=True)