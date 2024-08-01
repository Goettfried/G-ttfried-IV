from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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

def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

