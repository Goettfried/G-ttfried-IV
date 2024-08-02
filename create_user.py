from app import db, create_app
from app import User

app = create_app()

with app.app_context():
    username = "Nicolas"
    password = "Goetzinger"

    # Check if the user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
        print(f"L'utilisateur existant {username} a été supprimé.")

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    print(f"L'utilisateur {username} a été créé.")
