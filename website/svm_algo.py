from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json

import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn import svm

import base64

from .models import User, Datasets
from . import db
import os
import imghdr

svm_algo = Blueprint('svm_algo', __name__)

@svm_algo.route('/svm/model', methods=['GET', 'POST'])
def svm_model():
	# Load data
	current_dir = os.getcwd()
	current_dir += '\\website\\static\\upload\\'

	X = []
	y = []

	datasets = db.session.query(Datasets.ds_name, Datasets.ds_grade).group_by(Datasets.ds_name, Datasets.ds_grade).all()
	directories = [{'name': ds_grade + ' ' + ds_name , 'folder' : current_dir+ds_grade+'\\'+ds_name.lower()} for ds_name, ds_grade in datasets]

	print_ = []
	for index,folder in enumerate(directories):
		print(f"Images in {folder['name']}:")
		directory = folder['folder']
		for filename in os.listdir(directory):
			filepath = os.path.join(directory, filename)
			if os.path.isfile(filepath):
				filetype = imghdr.what(filepath)
				if filetype:
					images = cv2.imread(filepath)
					for_images = cv2.resize(images, (100, 100))
					X.append(cv2.cvtColor(for_images, cv2.COLOR_BGR2GRAY).flatten())
					y.append(index)
					print_.append(f"{filename} is an image file of type {filetype}")
				else:
					print_.append(f"{filename} is not an image file")
	X_train = np.array(X)
	y_train = np.array(y)

	X = []
	filepath = current_dir + '\\rotten\\durian\\Durian_20230419113006.png'
	images = cv2.imread(filepath)
	for_images = cv2.resize(images, (100, 100))
	X.append(cv2.cvtColor(for_images, cv2.COLOR_BGR2GRAY).flatten())

	X_test = np.array(X)

	# # Split data into training and testing sets
	# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

	# Train SVM model
	clf = svm.SVC(kernel='linear')
	clf.fit(X_train, y_train)

	# Test SVM model
	y_pred = clf.predict(X_test)
	result = directories[y_pred[0]]['name']
	# accuracy = clf.score(X_test, y_test)

	return jsonify(result)

def get_model():
	# Load data
	current_dir = os.getcwd()
	current_dir += '\\website\\static\\upload\\'

	X = []
	y = []

	datasets = db.session.query(Datasets.ds_name, Datasets.ds_grade).group_by(Datasets.ds_name, Datasets.ds_grade).all()
	directories = [{'name': ds_grade + ' ' + ds_name , 'folder' : current_dir+ds_grade+'\\'+ds_name.lower()} for ds_name, ds_grade in datasets]

	print_ = []
	for index,folder in enumerate(directories):
		directory = folder['folder']
		for filename in os.listdir(directory):
			filepath = os.path.join(directory, filename)
			if os.path.isfile(filepath):
				filetype = imghdr.what(filepath)
				if filetype:
					images = cv2.imread(filepath)
					for_images = cv2.resize(images, (100, 100))
					X.append(cv2.cvtColor(for_images, cv2.COLOR_BGR2GRAY).flatten())
					y.append(index)
	X_train = np.array(X)
	y_train = np.array(y)

	# # Split data into training and testing sets
	# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

	# Train SVM model
	clf = svm.SVC(kernel='linear')
	clf.fit(X_train, y_train)

	return clf,directories

@svm_algo.route('/svm/detect', methods=['GET', 'POST'])
def svm_detects():
    if request.method == "POST":
        cv_image = request.files["image"]
        file_data = cv_image.read()
        nparr = np.fromstring(file_data,np.uint8)
        images = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        for_images = cv2.resize(images, (100, 100))

        X = []
        X.append(cv2.cvtColor(for_images, cv2.COLOR_BGR2GRAY).flatten())
        X_test = np.array(X)
        clf,directories = get_model()
        y_pred = clf.predict(X_test)
        result = directories[y_pred[0]]['name']

        _, buffer = cv2.imencode('.jpg', images)
        img_str = base64.b64encode(buffer).decode()

        return render_template(
            "detect.html",
            display_style="display:block;",
            user=current_user,
            freshness_label=result.upper(),
            base64_image='data:image/jpg;base64, '+img_str,
        )
    return render_template("detect.html", user=current_user,display_style="display:none;")

@svm_algo.route('/api/detect', methods=['GET', 'POST'])
def svm_api_detects():
    if request.method == "POST":
    	img_file = request.form.get('img_file')
    	byte_str = base64.b64decode(img_file)
    	np_arr = np.frombuffer(byte_str, np.uint8)
    	images = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    	for_images = cv2.resize(images, (100, 100))
    	X = []
    	X.append(cv2.cvtColor(for_images, cv2.COLOR_BGR2GRAY).flatten())
    	X_test = np.array(X)
    	clf,directories = get_model()
    	y_pred = clf.predict(X_test)
    	result = directories[y_pred[0]]['name']
    	return jsonify({
    		"result":{
    			"freshness_percentage": result
    		}
    	})
    return ''
def imdecode_image(image_file):
    return cv2.imdecode(
        np.frombuffer(image_file.read(), np.uint8),
        cv2.IMREAD_UNCHANGED
    )