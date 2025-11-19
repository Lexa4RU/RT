from app import db, User
import bcrypt

def create_user(username, password, role="user"):
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()
    user = User(username=username, password_hash=password_hash, role=role)
    db.session.add(user)
    db.session.commit()
    print(f"Utilisateur {username} créé avec le rôle {role}.")

if __name__ == "__main__":
    print("Création d'un administrateur d'exemple…")
    create_user("admin", "progtr00", role="admin")

    print("Création d'un utilisateur normal d'exemple…")
    create_user("toto", "progtr00", role="user")
