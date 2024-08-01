from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os

auth = HTTPBasicAuth()

users = {
    os.environ.get('USERNAME'): generate_password_hash(os.environ.get('PASSWORD'))
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None