from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json
from flask import jsonify


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        fname = request.form.get('fname')
        mname = request.form.get('mname')
        lname = request.form.get('lname')

        update_user = {User.mname:mname,User.fname:fname,User.lname:lname}

        db.session.query(User).filter(User.id == user_id).update(update_user, synchronize_session = False)
        db.session.commit()
        flash('Profile updated!', category='success')
        return redirect(url_for('auth.profile'))

    # return redirect(url_for('auth.login'))
    return render_template("profile.html", user=current_user)

@auth.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        category = request.form.get('category')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        else:
            new_user = User(fname=first_name, mname=middle_name, lname=last_name, username=username, password=generate_password_hash(
                password, method='sha256'), category=category)
            db.session.add(new_user)
            db.session.commit()
            # login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.users'))

    users = User.query.all()
    return render_template("user.html", user=current_user, users=users)

@auth.route('/users/destroy', methods=['POST'])
@login_required
def delete_user():
    requestData = json.loads(request.data)
    requestID = requestData['userId'] 
    crime = User.query.get(requestID)
    db.session.delete(crime)
    db.session.commit()

    response_data = ""
    if current_user.id == requestID:
        response_data = "/logout"
    else:
        response_data = "/users"

    return jsonify({ "redirectTo": response_data })