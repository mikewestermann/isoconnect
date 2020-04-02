from models.settings import db
from datetime import datetime

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maschine = db.Column(db.String)
    text = db.Column(db.String)
    leistung = db.Column(db.Integer)
    spannung = db.Column(db.Integer)
    stromstaerke = db.Column(db.Integer)
    blechstaerke = db.Column(db.Integer)
    


    
