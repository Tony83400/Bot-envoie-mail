from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()

def get_paris_time():
    return datetime.now(pytz.timezone('Europe/Paris'))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    folder_path = db.Column(db.String(255), nullable=False)
    email_body = db.Column(db.Text, nullable=True)
    applications = db.relationship('Application', backref='category', lazy=True)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)
    contact_email = db.Column(db.String(150), nullable=False)
    contact_name = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='En attente') # En attente, Répondu, Relancé
    email_subject = db.Column(db.String(255), nullable=False)
