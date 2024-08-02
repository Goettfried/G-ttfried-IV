from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, migrate, init, stamp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.cli.command("init-db")
def init_db():
    """Initialise la base de données."""
    init()
    stamp()
    migrate(message="Initial migration")
    upgrade()
    print("Base de données initialisée")

if __name__ == '__main__':
    app.run(debug=True)