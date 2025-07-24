from . import db
from datetime import datetime

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    apartment_number = db.Column(db.String(20), nullable=False)
    rent_amount = db.Column(db.Float, nullable=False)
    due_day = db.Column(db.Integer, nullable=False)  # e.g. 5th of every month
    move_in_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class RentPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    month = db.Column(db.String(20), nullable=False)  # e.g., "2025-07"
    is_late = db.Column(db.Boolean, default=False)

    tenant = db.relationship('Tenant', backref='payments')
