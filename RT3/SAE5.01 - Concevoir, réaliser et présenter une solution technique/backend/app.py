from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import docker
import random
import psutil
from config import Config

# ------------------------------
# Flask Setup
# ------------------------------

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://tp_user:tp_password@localhost/tp_platform"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

client = docker.from_env()

# ------------------------------
# MODELS
# ------------------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="user")

    @property
    def is_admin(self):
        return self.role == "admin"

class ImageTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    docker_image = db.Column(db.String(200))
    description = db.Column(db.String(300))

class UserContainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    container_id = db.Column(db.String(64))
    name = db.Column(db.String(150))
    image = db.Column(db.String(200))
    port = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------------------
# Docker Utils
# ------------------------------

def get_free_port():
    return random.randint(30000, 40000)

def sanitize(name):
    import re
    return re.sub(r'[^a-zA-Z0-9_.-]', '-', name)

def launch_container_for_user(template: ImageTemplate, user: User):
    port = get_free_port()

    clean_template_name = sanitize(template.name)
    clean_username = sanitize(user.username)

    container_name = f"{clean_username}_{clean_template_name}_{port}"

    container = client.containers.run(
        template.docker_image,
        detach=True,
        ports={"80/tcp": ("127.0.0.1", port)},
        name=container_name,
        auto_remove=True,
        mem_limit="512m",
        network="tp_private_network",
    )

    record = UserContainer(
        user_id=user.id,
        container_id=container.id,
        name=container_name,
        image=template.docker_image,
        port=port
    )
    db.session.add(record)
    db.session.commit()

    return record

def stop_container(container_record, user):
    if not user.is_admin and container_record.user_id != user.id:
        abort(403)

    try:
        cont = client.containers.get(container_record.container_id)
        cont.kill()
    except:
        pass

    db.session.delete(container_record)
    db.session.commit()

# ------------------------------
# AUTH
# ------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = User.query.filter_by(username=request.form["username"]).first()
        if u and check_password_hash(u.password_hash, request.form["password"]):
            login_user(u)
            return redirect(url_for("user_images"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ------------------------------
# ADMIN — USERS
# ------------------------------

@app.route("/admin/users")
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)

    users = User.query.all()
    return render_template("admin_users.html", users=users)

@app.route("/admin/users/create", methods=["GET", "POST"])
@login_required
def admin_create_user():
    if not current_user.is_admin:
        abort(403)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        hashed = generate_password_hash(password)

        user = User(username=username, password_hash=hashed, role=role)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("admin_users"))

    return render_template("admin_create_user.html")

@app.route("/admin/users/delete/<int:user_id>")
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin:
        abort(403)

    if user_id == current_user.id:
        abort(403)  # interdit auto-suicide admin

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("admin_users"))

# ------------------------------
# ADMIN — IMAGES
# ------------------------------

@app.route("/admin/images", methods=["GET", "POST"])
@login_required
def admin_images():
    if not current_user.is_admin:
        abort(403)

    if request.method == "POST":
        template = ImageTemplate(
            name=request.form["name"],
            docker_image=request.form["docker_image"],
            description=request.form["description"]
        )
        db.session.add(template)
        db.session.commit()

    images = ImageTemplate.query.all()
    return render_template("admin_images.html", templates=images)


@app.route("/admin/containers")
@login_required
def admin_containers():
    if not current_user.is_admin:
        abort(403)

    containers = UserContainer.query.all()
    return render_template("admin_containers.html", containers=containers)

@app.route("/admin/kill/<int:id>")
@login_required
def admin_kill(id):
    if not current_user.is_admin:
        abort(403)

    record = UserContainer.query.get(id)
    stop_container(record, current_user)
    return redirect(url_for("admin_containers"))

# ------------------------------
# ADMIN — MONITORING
# ------------------------------

@app.route("/admin/monitoring")
@login_required
def admin_monitoring():
    if not current_user.is_admin:
        abort(403)

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    return render_template("monitoring.html", cpu=cpu, ram=ram, disk=disk)

# ------------------------------
# USER ROUTES
# ------------------------------

@app.route("/images")
@login_required
def user_images():
    images = ImageTemplate.query.all()
    return render_template("user_images.html", templates=images)

MAX_CONTAINERS = 10

@app.route("/launch/<int:image_id>")
@login_required
def user_launch(image_id):
    # Limite du nombre de conteneurs
    count = UserContainer.query.filter_by(user_id=current_user.id).count()
    if count >= MAX_CONTAINERS:
        return "You have reach the maximum limit of containers.", 403

    template = ImageTemplate.query.get_or_404(image_id)

    # Crée le container
    container_url = launch_container_for_user(template, current_user)

    # Récupère le dernier container créé par cet utilisateur
    container = UserContainer.query.filter_by(user_id=current_user.id).order_by(UserContainer.id.desc()).first()

    # Redirige vers la route open_container avec le bon ID
    return redirect(url_for("open_container", id=container.id))

@app.route("/open/<int:id>")
@login_required
def open_container(id):
    cont = UserContainer.query.get_or_404(id)

    if current_user.role != "admin" and cont.user_id != current_user.id:
        abort(403)

    return redirect(f"/container/{cont.id}")

@app.route("/mycontainers")
@login_required
def user_containers():
    containers = UserContainer.query.filter_by(user_id=current_user.id).all()
    return render_template("user_containers.html", containers=containers)

@app.route("/container/<int:id>")
@login_required
def proxy_container(id):
    cont = UserContainer.query.get_or_404(id)

    if current_user.role != "admin" and cont.user_id != current_user.id:
        abort(403)

    return render_template("proxy_container.html", port=cont.port)

@app.route("/kill/<int:id>")
@login_required
def user_kill(id):
    record = UserContainer.query.get_or_404(id)
    stop_container(record, current_user)
    return redirect(url_for("user_containers"))

# ------------------------------
# MAIN
# ------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
