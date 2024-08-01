from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

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

    # Process and store the data as needed
    print(f"Received data: {name}, {email}, {phone}, {message}")

    try:
        send_email(name, email, phone, message)
        return jsonify({'status': 'success', 'message': 'Form data received and email sent'}), 200
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to send email'}), 500

def send_email(name, email, phone, message):
    sender_email = 'your_email@example.com'
    receiver_email = 'receiver_email@example.com'
    password = 'your_password'

    msg = MIMEText(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")
    msg['Subject'] = 'New Form Submission'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == '__main__':
    app.run(debug=True)