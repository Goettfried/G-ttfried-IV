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

    # Traitez et stockez les données comme nécessaire
    print(f"Received data: {name}, {email}, {phone}, {message}")

    return jsonify({'status': 'success', 'message': 'Form data received'}), 200

if __name__ == '__main__':
    app.run(debug=True)