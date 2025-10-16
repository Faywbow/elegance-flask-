from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# Assurez-vous d'importer vos classes de formulaires depuis votre fichier forms.py
from forms import LoginForm, RegisterForm

app = Flask(__name__)

# La configuration est souvent dans un fichier config.py, mais pour l'exemple :
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'une_cle_secrete_tres_difficile_a_deviner'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
# Optionnel : redirige les utilisateurs non connectés vers la page de connexion
login_manager.login_view = 'login'

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
    # Crée une instance du formulaire de connexion
    form = LoginForm()
    # Ici, vous ajouterez la logique pour vérifier les informations de l'utilisateur
    # if form.validate_on_submit():
    #     # ... logique de connexion ...
    #     return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Crée une instance du formulaire d'inscription
    form = RegisterForm()
    # Ici, vous ajouterez la logique pour créer un nouvel utilisateur
    # if form.validate_on_submit():
    #     # ... logique d'inscription ...
    #     return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Gestionnaire pour les erreurs 500 (Erreur interne du serveur)
@app.errorhandler(500)
def internal_error(error):
    # Optionnel : vous pouvez ajouter un db.session.rollback() ici pour annuler les transactions en cas d'erreur
    # db.session.rollback()
    return render_template('error.html', message="Une erreur interne est survenue."), 500

# Le bloc if __name__ == '__main__': n'est pas nécessaire pour le déploiement sur Render,
# car Gunicorn est utilisé pour lancer l'application.
# Vous pouvez le garder pour tester en local.
if __name__ == '__main__':
    app.run(debug=True)
