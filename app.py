from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Importez vos classes de formulaires et de modèles depuis leurs fichiers respectifs
from forms import LoginForm, RegisterForm
from models import User 

app = Flask(__name__)

# Assurez-vous que ces configurations correspondent à votre fichier config.py ou à vos variables d'environnement
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # Ou votre URL de base de données Render
app.config['SECRET_KEY'] = 'une_cle_secrete_tres_difficile_a_deviner'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Redirige les utilisateurs non connectés vers la page de connexion

# --- CONFIGURATION ESSENTIELLE DE FLASK-LOGIN ---
# Cette fonction est obligatoire. Elle explique à Flask-Login comment
# retrouver un utilisateur spécifique à partir de l'ID stocké dans la session.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# ----------------------------------------------------

# --- VOS ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Mettez votre logique de validation et de connexion ici
    # if form.validate_on_submit():
    #     ...
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # Mettez votre logique de création d'utilisateur ici
    # if form.validate_on_submit():
    #     ...
    return render_template('register.html', form=form)

# --- GESTION DES ERREURS ---

@app.errorhandler(500)
def internal_error(error):
    # En cas d'erreur interne, cette page sera affichée
    return render_template('error.html', message="Une erreur interne inattendue est survenue."), 500

@app.errorhandler(404)
def page_not_found(error):
    # Pour les pages non trouvées (erreur 404)
    return render_template('error.html', message="Cette page n'existe pas."), 404

# Cette partie n'est pas utilisée par Render mais est utile pour les tests locaux
if __name__ == '__main__':
    app.run(debug=True)
