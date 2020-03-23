from models.settings import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String) 
    nachname = db.Column(db.String)
    unternehmen = db.Column(db.String)
    position = db.Column(db.String)
    email_adresse = db.Column(db.String, unique=True)
    passwort_hash = db.Column(db.String)
    session_token = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.utcnow)
