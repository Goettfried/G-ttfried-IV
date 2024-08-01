from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    travail_data = FormData.query.filter_by(type="Je recherche du travail").all()
    stage_data = FormData.query.filter_by(type="Je recherche un stage").all()
    return render_template('index.html', travail_data=travail_data, stage_data=stage_data)

@app.route('/init_db')
def init_db():
    db.create_all()
    return "Database initialized!"

@app.route('/check_tables')
def check_tables():
    try:
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        return f"Tables: {tables}"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)

