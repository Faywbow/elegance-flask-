from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    """
    Formulaire pour l'inscription des utilisateurs.
    """
    # Chaque champ est indenté de 4 espaces pour être à l'intérieur de la classe
    username = StringField(
        'Nom d\'utilisateur', 
        validators=[
            DataRequired(message="Ce champ est obligatoire."), 
            Length(min=4, max=25, message="Le nom d'utilisateur doit contenir entre 4 et 25 caractères.")
        ]
    )
    email = StringField(
        'Adresse e-mail', 
        validators=[
            DataRequired(message="Ce champ est obligatoire."), 
            Email(message="Veuillez entrer une adresse e-mail valide.")
        ]
    )
    password = PasswordField(
        'Mot de passe', 
        validators=[
            DataRequired(message="Ce champ est obligatoire."), 
            Length(min=6, message="Le mot de passe doit contenir au moins 6 caractères.")
        ]
    )
    confirm_password = PasswordField(
        'Confirmer le mot de passe', 
        validators=[
            DataRequired(message="Ce champ est obligatoire."), 
            EqualTo('password', message="Les mots de passe ne correspondent pas.")
        ]
    )
    submit = SubmitField('S\'inscrire')


class LoginForm(FlaskForm):
    """
    Formulaire pour la connexion des utilisateurs.
    """
    # L'indentation est également cruciale ici
    email = StringField(
        'Adresse e-mail', 
        validators=[
            DataRequired(message="Ce champ est obligatoire."), 
            Email(message="Veuillez entrer une adresse e-mail valide.")
        ]
    )
    password = PasswordField(
        'Mot de passe', 
        validators=[DataRequired(message="Ce champ est obligatoire.")]
    )
    submit = SubmitField('Se connecter')
