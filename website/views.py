from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json
from werkzeug.utils import secure_filename
import os
from .models import User, Datasets, ScannedFruits
from . import db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/datasets', methods=['GET', 'POST'])
def datasets():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'ds_image' not in request.files:
            flash('No selected file')
            return redirect(url_for('views.datasets'))

        ds_name = request.form.get('ds_name')
        ds_freshness = request.form.get('ds_freshness')
        file = request.files['ds_image']

        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('views.datasets'))

        if file and allowed_file(file.filename):
            now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            new_upload_folder = UPLOAD_FOLDER+ds_freshness+"/"+ds_name.lower()+"/"
            os.makedirs(os.path.dirname(new_upload_folder), exist_ok=True)

            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[-1]
            new_file_name = ds_name+"_"+now+"."+file_extension
            filePath = os.path.join(new_upload_folder, new_file_name)
            file.save(filePath)

            new_slug = filePath.replace("website", '')

            # add to database
            datasets = Datasets(ds_name=ds_name, ds_grade=ds_freshness, slug=new_slug)
            db.session.add(datasets)
            db.session.commit()

            flash('Dataset Added!', category='success')
            return redirect(url_for('views.datasets'))

    datasets = Datasets.query.all()
    return render_template("datasets.html", user=current_user, datasets=datasets)
@views.route('/scan', methods=['GET', 'POST'])
def scan():
    datasets = ScannedFruits.query.all()
    return render_template("scan.html", user=current_user, datasets=datasets)

@views.route('/dataset/destroy', methods=['POST'])
@login_required
def delete_dataset():
    requestData = json.loads(request.data)
    requestID = requestData['dsId'] 
    dsdata = Datasets.query.get(requestID)

    if(dsdata.slug is not None):
        if os.path.exists("website"+dsdata.slug):
            os.remove("website"+dsdata.slug)

    db.session.delete(dsdata)
    db.session.commit()

    flash('Dataset deleted', category="success")
    return jsonify({ "delete_response": "deleted" })

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS