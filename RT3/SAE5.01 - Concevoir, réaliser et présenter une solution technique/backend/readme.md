This Flask application provides a platform for users to manage Docker containers. Users can log in, create and manage their own containers based on pre-defined Docker image templates, and view the status of their containers. Administrators have additional privileges to manage users, monitor system performance, and kill any running containers.

The application is deployed using Nginx as a reverse proxy and Gunicorn as the WSGI server to handle incoming HTTP requests.

1. Flask Setup

 
a    
 
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://tp_user:tp_password@localhost/tp_platform"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    client = docker.from_env()


Flask: Initializes the Flask application.

SQLAlchemy: Configures the database connection and models.

LoginManager: Manages user authentication and sessions.

Docker client: Connects to the Docker engine for container management.

2. Database Models

The application has three key database models: User, ImageTemplate, and UserContainer.

    User Model
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)
        role = db.Column(db.String(10), nullable=False, default="user")


User: Represents a user in the system with username, password_hash, and role (admin or user).

    ImageTemplate Model
    class ImageTemplate(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), unique=True)
        docker_image = db.Column(db.String(200))
        description = db.Column(db.String(300))


ImageTemplate: Represents a Docker image template with a name, associated Docker image, and description.

    UserContainer Model
    class UserContainer(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer)
        container_id = db.Column(db.String(64))
        name = db.Column(db.String(150))
        image = db.Column(db.String(200))
        port = db.Column(db.Integer)


UserContainer: Represents a Docker container running for a specific user, containing information about the container's ID, name, image, and port.

3. Authentication & Authorization
Login and Logout

Login (/login): Authenticates a user and starts a session.

Logout (/logout): Logs the user out and redirects to the login page.

The login functionality checks if the user exists and verifies the password using check_password_hash.

Admin Check

Many routes require administrative privileges. The check is done with the is_admin property in the User model:

    @property
    def is_admin(self):
        return self.role == "admin"

4. Docker Utility Functions
Launch and Stop Containers

launch_container_for_user: Launches a Docker container based on a selected image template and assigns it to a user. The container is configured with specific memory and network settings.

stop_container: Stops a running container and removes its record from the database. Only the admin or the user who created the container can stop it.

    def launch_container_for_user(template: ImageTemplate, user: User):
        # Create and start a Docker container
        ...

    def stop_container(container_record, user):
        # Stop the container and remove its record from the database
        ...

5. Routes

The app has routes for both regular users and administrators.

User Routes

    /images: Displays available image templates to the user.

    /launch/<int:image_id>: Launches a container from a selected image template.

    /open/<int:id>: Redirects to the URL of the container's proxy page.

    /mycontainers: Displays the user's containers.

    /kill/<int:id>: Stops and deletes the user's container.

Admin Routes

    /admin/users: List all users in the system.

    /admin/users/create: Allows the admin to create a new user.

    /admin/users/delete/<int:user_id>: Allows the admin to delete a user.

    /admin/images: Displays all available image templates and allows the admin to create new ones.

    /admin/containers: Displays all containers in the system.

    /admin/kill/<int:id>: Allows the admin to kill a container.

    /admin/monitoring: Displays system resource usage (CPU, RAM, and Disk).

Container Proxy

    /container/<int:id>: Proxy route that redirects to the container's web interface.

6. Admin Monitoring

/admin/monitoring: Shows the server's resource usage (CPU, RAM, disk) using the psutil library.

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

7. Docker Container Management

The app integrates with Docker to manage containers for each user:

Container Creation: When a user launches a container, a new Docker container is started based on a template. The container is mapped to a random available port on the host.

Container Stopping: Only an admin or the user who created the container can stop it. The container is removed from the system once stopped.

8. Configuration

The configuration settings are loaded from a Config class, which may include sensitive data such as database URIs, secret keys, etc. This configuration is typically set in a separate config.py file.

    class Config:
        SECRET_KEY = 'your_secret_key_here'
        # Other configurations like database URI

9. Running the Application

This Flask app is deployed using Gunicorn as the WSGI server, which allows it to handle multiple requests concurrently. Nginx serves as a reverse proxy, routing requests to Gunicorn. The typical deployment setup would look like this:

Nginx: Acts as a reverse proxy to forward requests from clients to the Gunicorn workers.

Gunicorn: A Python WSGI HTTP Server that runs the Flask application and manages multiple worker processes to handle requests.

Steps for Deployment:

Install Gunicorn:
You need to install Gunicorn in your environment.

    pip install gunicorn


Run Gunicorn:
Launch the application using Gunicorn with multiple worker processes.

    gunicorn -w 4 app:app


The -w 4 option specifies that Gunicorn should run 4 worker processes. This helps to handle multiple requests concurrently.

Nginx Configuration:
Configure Nginx to forward HTTP requests to the Gunicorn server. Below is an example of an Nginx configuration file (/etc/nginx/sites-available/your_app):

    server {
        listen 443 ssl;
        server_name _;

        ssl_certificate /etc/nginx/ssl/server.crt;
        ssl_certificate_key /etc/nginx/ssl/server.key;

        location /_proxy/ {
            rewrite ^/_proxy/([0-9]+)/?(.*)$ /$2 break;
            proxy_pass http://127.0.0.1:$1;

            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }

            location /container/ {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
        }

        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
        }
    }  

    server {
        listen 80;
        return 301 https://$host$request_uri;
    }

Restart Nginx:
After updating the Nginx configuration, restart the Nginx service.

    sudo systemctl restart nginx


Now, your Flask app is served by Nginx, with Gunicorn running as the backend server to handle incoming requests.

10. Security

The app uses password hashing (via werkzeug.security) to securely store user passwords. Additionally, it implements role-based access control, ensuring that only authorized users (admins) can perform certain operations, such as managing users and containers.

11. Example Workflow

User Login: A user logs in using their credentials.

View Image Templates: The user is shown a list of available Docker image templates.

Launch Container: The user selects an image and launches a container.

Container Management: The user can view, open, or stop their own containers.

12. Troubleshooting

Gunicorn Performance: Adjust the number of worker processes in Gunicorn based on your server’s hardware specifications. If your app is receiving high traffic, consider increasing the number of workers.

Nginx Logs: Check the Nginx logs (/var/log/nginx/) for errors if the app is not accessible via the web.

Container Logs: You can monitor the logs of your Docker containers to troubleshoot any issues related to container startup or execution.
