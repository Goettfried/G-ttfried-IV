from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Modèle User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Modèle FormData
class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    message = db.Column(db.Text, nullable=False)
    submission_type = db.Column(db.String(50), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            app.logger.debug(f"Trying to log in with username: {username}")
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['username'] = user.username
                return redirect(url_for('index'))
            else:
                return 'Invalid username or password'
        except Exception as e:
            app.logger.error(f"Error during login: {e}")
            return 'Internal Server Error', 500
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/protected')
def protected():
    if 'username' in session:
        return render_template('protected.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/receive_form', methods=['POST'])
def receive_form():
    try:
        data = request.get_json()
        app.logger.debug(f"Received data: {data}")
        if data:
            form_data = FormData(
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone'),
                message=data.get('message'),
                submission_type=data.get('form_type')
            )
            db.session.add(form_data)
            db.session.commit()
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/view_data')
def view_data():
    if 'username' in session:
        form_data = FormData.query.all()
        return render_template('view_data.html', form_data=form_data)
    return redirect(url_for('login'))

@app.route('/export_data')
def export_data():
    # Implémentez l'export des données ici
    pass

if __name__ == '__main__':
    app.run(debug=True)

