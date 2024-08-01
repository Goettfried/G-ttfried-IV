import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify

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

    print(f"Received data: {name}, {email}, {phone}, {message}")

    if send_email(name, email, phone, message):
        return jsonify({'status': 'success', 'message': 'Form data received and email sent'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to send email'}), 500

def send_email(name, email, phone, message):
    try:
        sender_email = os.environ.get('EMAIL_USER')
        receiver_email = 'votre_email_de_réception@example.com'  # Remplacez par l'email du destinataire
        password = os.environ.get('EMAIL_PASS')

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = 'New Contact Form Submission'

        body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email envoyé avec succès")
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True)