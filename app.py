from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    message = db.Column(db.Text)
    type = db.Column(db.String(50))

@app.route('/')
def index():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    service_data = FormData.query.filter_by(type="Je propose mes services").all()
    return render_template('index.html', travail_data=travail_data, service_data=service_data)

@app.route('/init_db')
def init_db():
    db.drop_all()  # Supprimer toutes les tables existantes
    db.create_all()  # Créer toutes les tables
    return "Database initialized!"

@app.route('/check_tables')
def check_tables():
    tables = db.engine.table_names()
    return f"Tables: {tables}"

if __name__ == '__main__':
    app.run(debug=True)

