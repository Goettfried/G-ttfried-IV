from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/receive_form', methods=['POST'])
def receive_form():
    data = request.get_json()
    if data:
        print(f"Received data: {data}")
        return jsonify({"status": "success", "message": "Form data received"}), 200
    return jsonify({"status": "error", "message": "No data received"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))