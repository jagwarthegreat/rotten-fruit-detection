from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'tbl_user'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(150))
    mname = db.Column(db.String(150))
    lname = db.Column(db.String(150))
    address = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    category = db.Column(db.String(150))
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
