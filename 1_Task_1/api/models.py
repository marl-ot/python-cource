# from sqlalchemy import Column, Integer, String, Date, Boolean
from app import db

class BankCard(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(16))
    end_date = db.Column(db.Date)
    cvv  = db.Column(db.String)
    card_type  = db.Column(db.String(32))
    person  = db.Column(db.String(64))
    is_active  = db.Column(db.Boolean)

    def to_dict(self):
        return {
            "card_id": self.card_id,
            "card_number": self.card_number,
            "end_date": str(self.end_date.strftime('%d-%m-%Y')),
            "cvv": self.cvv,
            "card_type": self.card_type,
            "person": self.person,
            "is_active": self.is_active
        }