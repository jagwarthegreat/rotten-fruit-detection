from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from .models import User, Datasets
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import json
from werkzeug.utils import secure_filename
import os

api = Blueprint('api', __name__)

@api.route('/login', methods=['GET', 'POST'])
def apiLogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                return jsonify({ "result": user.id })
            else:
                return jsonify({ "result": "Incorrect password, try again." })
        else:
            return jsonify({ "result": "Username does not exist." })

    return jsonify({ "result": "test api login result" })

@api.route('/register', methods=['GET','POST'])
def apiRegister():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        category = request.form.get('category')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({ "result": "Username already exists" })
        else:
            new_user = User(fname=first_name, mname=middle_name, lname=last_name, username=username, address=address, password=generate_password_hash(
                password, method='sha256'), category=category)
            db.session.add(new_user)
            db.session.commit()
            # login_user(new_user, remember=True)
            return jsonify({ "result": new_user.id })

    return jsonify({ "result": "test api register result" })

@api.route('/getprofile', methods=['GET', 'POST'])
def apiProfile():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        return jsonify({
            "first_name": user.fname,
            "middle_name": user.mname,
            "last_name": user.lname,
            "address": user.address,
            "username": user.username,
        })

@api.route('/password', methods=['GET', 'POST'])
def apiPassword():
    return jsonify({ "result": "this is api password" })