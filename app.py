import os
from flask import Flask, render_template, redirect, url_for, flash, request,
jsonify
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from models import db, User, Reservation
from forms import RegisterForm, LoginForm, ReservationForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required,
logout_user, current_user
import stripe
def create_app():
app = Flask(__name__, static_folder="static",
template_folder="templates")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', SECRET_KEY)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
SQLALCHEMY_DATABASE_URI)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
# Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
@login_manager.user_loader
def load_user(user_id):
return User.query.get(int(user_id))
@app.context_processor
def inject_now():
from datetime import datetime
return {'current_year': datetime.utcnow().year, 'stripe_public_key':
STRIPE_PUBLIC_KEY}
@app.route('/')
def index():
return render_template('index.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
form = RegisterForm()
if form.validate_on_submit():
if User.query.filter((User.email == form.email.data) |
4
(User.username == form.username.data)).first():
flash('Un utilisateur avec ce nom ou email existe déjà.',
'warning')
return redirect(url_for('register'))
user = User(
username=form.username.data,
email=form.email.data,
password_hash=generate_password_hash(form.password.data)
)
db.session.add(user)
db.session.commit()
flash('Inscription réussie — connecte-toi !', 'success')
return redirect(url_for('login'))
return render_template('register.html', form=form)
@app.route('/login', methods=['GET', 'POST'])
def login():
form = LoginForm()
if form.validate_on_submit():
user = User.query.filter_by(email=form.email.data).first()
if user and check_password_hash(user.password_hash,
form.password.data):
login_user(user)
flash('Connecté avec succès.', 'success')
next_page = request.args.get('next')
return redirect(next_page or url_for('dashboard'))
flash('Email ou mot de passe invalide.', 'danger')
return render_template('login.html', form=form)
@app.route('/logout')
@login_required
def logout():
logout_user()
flash('Déconnecté.', 'info')
return redirect(url_for('index'))
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
form = ReservationForm()
if form.validate_on_submit():
r = Reservation(title=form.title.data, details=form.details.data,
user=current_user)
db.session.add(r)
db.session.commit()
flash('Réservation créée.', 'success')
return redirect(url_for('dashboard'))
reservations =
Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.created_at.desc()).areturn render_template('dashboard.html', form=form,
reservations=reservations)
5
# Stripe checkout route
@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
try:
# Amount en centimes
amount_cents = int(request.form.get('amount', 2000))
# Crée la session checkout
checkout_session = stripe.checkout.Session.create(
payment_method_types=["card"],
mode="payment",
line_items=[{
"price_data": {
"currency": "eur",
"product_data": {"name": "Accès Premium - Élégance"},
"unit_amount": amount_cents,
},
"quantity": 1,
}],
success_url=url_for('success', _external=True) + '?
session_id={CHECKOUT_SESSION_ID}',
cancel_url=url_for('cancel', _external=True),
customer_email=current_user.email
)
return redirect(checkout_session.url, code=303)
except Exception as e:
return jsonify(error=str(e)), 400
@app.route('/success')
@login_required
def success():
# Ici, on pourrait vérifier session via Stripe API pour confirmer le
paiement
flash('Paiement réussi ! Merci pour votre confiance ', 'success')
return render_template('success.html')
@app.route('/cancel')
@login_required
def cancel():
flash('Paiement annulé.', 'warning')
return render_template('cancel.html')
return app
if __name__ == '__main__':
app = create_app()
app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)),
debug=True)
