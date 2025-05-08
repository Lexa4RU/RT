from markupsafe import escape
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash
import mysql.connector
from mysql.connector import Error
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import hashlib

app = Flask(__name__)

# Configuration de la clé secrète pour JWT
app.config['JWT_SECRET_KEY'] = 'AlphaTango00'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)  # Expiration du token 30 minutes après sa création 
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'                      # Chemin où le cookie (token) fourni avec JWT sera valide
app.config['JWT_COOKIE_CSRF_PROTECT'] = False                   # Désactive la protection CSRF pour les cookies JWT
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'    # Nom du cookie pour le token d'accès

jwt = JWTManager(app)

# Configuration de la base de données
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',                   # Hôte de la base de données
            database='gestion_competences',     # Nom de la base de données MySQL
            user='lev',                         # Identifiant pour se connecter à la base de données
            password='progtr00'                 # Mot de passe pour se connecter à la base de données
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Erreur lors de la connection à la base de données MySQL : ", e)
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = hashlib.sha256((escape(request.form['password'])).encode('utf-8')).hexdigest()

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            if user:
                access_token = create_access_token(identity=username)
                response = make_response(redirect(url_for('competences')))
                response.set_cookie('access_token_cookie', access_token, httponly=True, secure=app.config['JWT_COOKIE_SECURE'])
                return response
            else:
                error = "Utilisateur ou mot de passe invalide"
        else:
            error = 'Database connection error'
    return render_template('login.html', error=error)

@app.route('/competences')
@jwt_required(optional=True)
def competences():
    current_user = get_jwt_identity()
    if not current_user:
        return redirect('/login')
    
    # Code existant pour récupérer et afficher les compétences
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        # Récupérer les semestres, blocs de compétences et compétences depuis la base de données
        cursor.execute("SELECT * FROM Semestres")
        semestres = cursor.fetchall()
        
        for semestre in semestres:
            cursor.execute("SELECT * FROM BlocsCompetences WHERE code_semestre = %s", (semestre['code_semestre'],))
            blocs = cursor.fetchall()
            semestre['blocs'] = blocs
            
            for bloc in blocs:
                cursor.execute("SELECT * FROM Competences WHERE code_bloc = %s", (bloc['code_bloc'],))
                competences = cursor.fetchall()
                bloc['competences'] = competences
                
                for competence in competences:
                    cursor.execute("SELECT * FROM NiveauxAcquisition WHERE code_competence = %s", (competence['code_competence'],))
                    niveaux = cursor.fetchall()
                    competence['niveaux'] = niveaux
        
        cursor.close()
        connection.close()
        return render_template('competences.html', semestres=semestres)
    else:
        return "Error connecting to the database"

@app.route('/ajouter_competence', methods=['POST'])
@jwt_required()
def ajouter_competence():
    semestre_code = escape(request.form['semestre'])
    bloc_code = escape(request.form['bloc'])
    competence_nom = escape(request.form['competence'])
    niveau_acquisition = escape(request.form['niveau'])

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Competences WHERE code_bloc = %s", (bloc_code,))
        count = cursor.fetchone()[0] + 1
        competence_code = f"{bloc_code}.{'%02d' % count}"
        
        cursor.execute(
            "INSERT INTO Competences (code_competence, nom_competence, code_bloc) VALUES (%s, %s, %s)",
            (competence_code, competence_nom, bloc_code)
        )
        
        cursor.execute(
            "INSERT INTO NiveauxAcquisition (niveau_acquisition, code_competence) VALUES (%s, %s)",
            (niveau_acquisition, competence_code)
        )
        
        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/competences')
    else:
        return "Error connecting to the database"

@app.route('/supprimer_competence', methods=['POST'])
@jwt_required()
def supprimer_competence():
    competence_code = escape(request.form['competence_code'])

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()

        # Supprimer les niveaux d'acquisition associés à la compétence
        cursor.execute("DELETE FROM NiveauxAcquisition WHERE code_competence = %s", (competence_code,))

        # Supprimer la compétence
        cursor.execute("DELETE FROM Competences WHERE code_competence = %s", (competence_code,))

        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/competences')
    else:
        return "Error connecting to the database"


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('access_token_cookie')
    return response

@app.route('/cv')
def cv():
    return render_template('cv.html')

@app.route('/hobby')
def hobby():
    return render_template('hobby.html')

@app.route('/conditions_utilisation')
def conditions_utilisation():
    return render_template('conditions_utilisation.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
