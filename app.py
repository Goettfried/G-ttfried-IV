from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/receive_form', methods=['POST'])
def receive_form():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')
    
    try:
        send_email(name, email, phone, message)
        return jsonify({"message": "Form data received", "status": "success"})
    except Exception as e:
        return jsonify({"message": f"Failed to send email: {str(e)}", "status": "error"}), 500

def send_email(name, email, phone, message):
    sender_email = "votre_email@gmail.com"
    receiver_email = "destinataire@example.com"
    password = "votre_mot_de_passe_d'application"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Nouveau message de contact"
    
    body = f"Nom: {name}\nEmail: {email}\nTéléphone: {phone}\nMessage: {message}"
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

if __name__ == '__main__':
    app.run(debug=True)