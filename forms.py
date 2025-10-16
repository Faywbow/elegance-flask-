from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
class RegisterForm(FlaskForm):
username = StringField('Nom d\'utilisateur', validators=[DataRequired(),
Length(3, 80)])
email = StringField('Email', validators=[DataRequired(), Email(),
Length(max=200)])
password = PasswordField('Mot de passe', validators=[DataRequired(),
Length(6, 128)])
confirm = PasswordField('Confirmer', validators=[DataRequired(),
EqualTo('password')])
submit = SubmitField('S\'inscrire')
class LoginForm(FlaskForm):
email = StringField('Email', validators=[DataRequired(), Email()])
password = PasswordField('Mot de passe', validators=[DataRequired()])
submit = SubmitField('Se connecter')
class ReservationForm(FlaskForm):
title = StringField('Titre', validators=[DataRequired(),
Length(max=200)])
details = TextAreaField('Détails (optionnel)',
validators=[Length(max=2000)])
submit = SubmitField('Réserver')
