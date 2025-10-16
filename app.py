# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import stripe

app = Flask(__name__)

# --- Configuration Flask & Base de données ---
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devkey')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Modèle de base de données ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

# --- Stripe configuration ---
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")

# --- Création automatique des tables au démarrage ---
with app.app_context():
    db.create_all()
    print("✅ Tables créées ou déjà existantes dans la base PostgreSQL")

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html", stripe_public_key=STRIPE_PUBLIC_KEY)

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return "Erreur : nom et email requis", 400

    # Vérifie si l'utilisateur existe déjà
    existing = User.query.filter_by(email=email).first()
    if existing:
        return "Cet email est déjà enregistré", 400

    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': 'Service Premium',
                    },
                    'unit_amount': 5000,  # prix en centimes = 50,00 €
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/cancel")
def cancel():
    return render_template("cancel.html")

# --- Lancement de l'app ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
