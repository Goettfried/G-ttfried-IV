from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Stocker les données reçues
form_data = {
    "Je recherche du travail": [],
    "Je recherche du personnel": []
}

@app.route('/')
def index():
    return render_template('index.html', data=form_data)

@app.route('/receive_form', methods=['POST'])
def receive_form():
    data = request.get_json()
    if data:
        form_type = data.get('type')
        if form_type in form_data:
            form_data[form_type].append(data)
        print(f"Received data: {data}")
        return jsonify({"status": "success", "message": "Form data received"}), 200
    return jsonify({"status": "error", "message": "No data received"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))