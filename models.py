from flask_sqlalchemy import SQLAlchemy
from server import app

db = SQLAlchemy(app)

class tblsymbols(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbols = db.Column(db.String)
    capital = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    sma = db.Column(db.Integer)
    lma = db.Column(db.Integer)
    interval = db.Column(db.String)
    startdt = db.Column(db.String)
    enddt = db.Column(db.String)

    def __init__(self, symbols, capital, quantity, sma, lma, interval, startdt, enddt):
        self.symbols = symbols
        self.capital = capital
        self.quantity = quantity
        self.sma = sma
        self.lma = lma
        self.interval = interval
        self.startdt = startdt
        self.enddt = enddt