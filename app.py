import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import stripe

# Initialisation de l’application Flask
app = Flask(__name__)

# Configuration générale
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev_secret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///database.db").replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Base de données
db = SQLAlchemy(app)

# Stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")

# Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# --- Modèle utilisateur ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# --- Gestion du chargement utilisateur ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes principales ---
@app.route("/")
def index():
    return render_template("index.html", stripe_public_key=STRIPE_PUBLIC_KEY)

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# --- Authentification ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        flash("Email ou mot de passe incorrect.")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Cet utilisateur existe déjà.")
            return redirect(url_for("register"))

        new_user = User(email=email, password=generate_password_hash(password, method="sha256"))
        db.session.add(new_user)
        db.session.commit()
        flash("Inscription réussie ! Vous pouvez vous connecter.")
        return redirect(url_for("login"))
    return render_template("register.html")

# --- Paiement Stripe ---
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': 'Produit Élégance'},
                    'unit_amount': 1999,  # 19,99€
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('cancel', _external=True),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/cancel")
def cancel():
    return render_template("cancel.html")

# --- Commande création BDD ---
@app.cli.command("init-db")
def init_db():
    """Initialise la base de données."""
    db.create_all()
    print("✅ Base de données initialisée avec succès.")

# --- Lancement ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/")
def index():
    return render_template("index.html")

