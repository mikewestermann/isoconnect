from models.settings import db
from datetime import datetime


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    baujahr = db.Column(db.String)
    maschinennummer = db.Column(db.Integer)
    standort = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # foreign key (table name for the User model is "users")
    author = db.relationship("User")  # not a real field, just shows a relationship with the User model
    machine_id = db.Column(db.Integer, db.ForeignKey("machines.id")) #One-to-many relationship zwischen vielen Cards und einer Machine
    machine = db.relationship("Machine")
    created = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, name, baujahr, maschinennummer, standort, author,machine):
        card = cls(name=name, baujahr=baujahr, maschinennummer=maschinennummer, standort=standort, author=author, machine=machine)
        db.add(card)
        db.commit()

        return card


