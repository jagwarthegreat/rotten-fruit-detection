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

class Datasets(db.Model):
    __tablename__ = 'tbl_datasets'
    ds_id = db.Column(db.Integer, primary_key=True)
    ds_name = db.Column(db.String(150))
    ds_grade = db.Column(db.Text())
    slug = db.Column(db.Text())
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())

class ScannedFruits(db.Model):
    __tablename__ = 'tbl_scanned_fruits'
    scan_id = db.Column(db.Integer, primary_key=True)
    scan_img = db.Column(db.Text())
    fruit_grade = db.Column(db.String(50))
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())

    @classmethod
    def add_new_fruit(cls, scan_img, fruit_grade):
        new_fruit = ScannedFruits(scan_img=scan_img, fruit_grade=fruit_grade)
        db.session.add(new_fruit)
        db.session.commit()