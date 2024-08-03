from app import db, User, app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

username = 'Nicolas'
password = 'Goetzinger'

with app.app_context():
    # Supprimer l'utilisateur existant
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print(f"User {username} deleted successfully!")
    
    # Créer un nouvel utilisateur avec le mot de passe haché
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    print(f"User {username} created successfully!")