from app import db, User
from flask_bcrypt import generate_password_hash

# Create a user
username = 'Nicolas'
password = 'Goetzinger'
hashed_password = generate_password_hash(password).decode('utf-8')

user = User(username=username, password_hash=hashed_password)

# Add the user to the session and commit
with app.app_context():
    db.session.add(user)
    db.session.commit()

print("User created successfully!")
