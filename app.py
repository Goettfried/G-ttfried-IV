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
    form_type = data.get('type')

    if not all([name, email, message, form_type]):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    send_email(name, email, phone, message, form_type)

    return jsonify({'status': 'success', 'message': 'Form data received'}), 200

def send_email(name, email, phone, message, form_type):
    sender_email = os.getenv('EMAIL_USER')
    receiver_email = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')

    subject = ""
    text = ""
    if form_type == "Je recherche du personnel":
        subject = "Merci pour votre démarche - Recherche de personnel"
        text = f"""
        Bonjour {name} ! 

        Je vous souhaite la bienvenue, merci pour votre démarche. 
        Si vous êtes intéressé(e) par mes prestations de placement fixe, je vous invite à consulter ce lien, qui vous mènera à mes conditions générales : https://welshrecrutement.netlify.app/conditions_generales_nicolas_ballu.pdf. 
        Si vous êtes plutôt intéressé(e) par de la location de services, ignorez ça pour le moment : je vous invite à me soumettre le nombre de travailleurs dont vous aurez besoin ainsi que la durée de leur mission, puis je prendrai rapidement contact avec vous. 

        Je me réjouis de faire affaire avec vous.

        Meilleures salutations.
        """
    else:
        subject = "Merci pour votre démarche - Recherche de travail"
        text = f"""
        Bonjour {name} ! 

        Je vous souhaite la bienvenue, merci pour votre démarche. 
        Je vais prendre contact avec vous très prochainement. 
        Pour aller de l'avant, j'aimerais vous demander de me soumettre votre dossier complet, comportant CV, attestation/certificats de travail et diplôme. 
        Je serais enchanté de vous aider.

        Meilleures salutations.
        """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print("Email envoyé avec succès")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")

if __name__ == '__main__':
    app.run(debug=True)