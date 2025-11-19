from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    u = User(username="admin", password_hash=generate_password_hash("progtr00"), role="admin")
    db.session.add(u)
    db.session.commit()
    print("Admin OK")
