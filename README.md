# Elegance Flask
Projet Flask avec système d'inscription, réservations et paiement Stripe.
## Installation locale
1. python -m venv venv
2. source venv/bin/activate # ou venv\Scripts\activate
3. pip install -r requirements.txt
4. export SECRET_KEY="une_valeur_secrete"
 export STRIPE_SECRET_KEY="sk_test_..."
 export STRIPE_PUBLIC_KEY="pk_test_..."
5. python init_db.py
6. python app.py
## Déploiement sur Render
- Pousser le repo sur GitHub
- Sur Render: New -> Web Service -> connect GitHub -> sélectionner le repo
- Build command: pip install -r requirements.txt
- Start command: python app.py
- Ajouter les variables d'environnement: SECRET_KEY, STRIPE_SECRET_KEY,
STRIPE_PUBLIC_KEY, DATABASE_URL (si PostgreSQL)
- Si PostgreSQL: create DB service on Render and set DATABASE_URL
- Lancer `python init_db.py` via Render shell pour créer les tables
## Tests Stripe (mode test)
- Carte test: 4242 4242 4242 4242, date future, CVC 123
