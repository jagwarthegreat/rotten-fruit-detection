from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Response
from flask_login import login_required, current_user
import json

import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn import svm
import joblib

import base64

from .models import User, Datasets, ScannedFruits
from . import db
import os
import imghdr

svm_algo = Blueprint('svm_algo', __name__)

img_file_size = (100,100)
window_name = "Fruit Rotten Detection using SVM"
def extract_features(img):
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).flatten()
    # hog = cv2.HOGDescriptor((64,64), (16,16), (8,8), (8,8), 9)
    # hist = hog.compute(img)
    # return hist.flatten()
@svm_algo.route('/svm/model', methods=['GET', 'POST'])
def svm_model():
	# Load data
	current_dir = os.getcwd()
	current_dir += '\\website\\static\\upload\\'

	X = []
	y = []

	datasets = db.session.query(Datasets.ds_name, Datasets.ds_grade).group_by(Datasets.ds_name, Datasets.ds_grade).all()
	directories = [{'name': ds_grade + ' ' + ds_name , 'folder' : current_dir+ds_grade+'\\'+ds_name.lower()} for ds_name, ds_grade in datasets]
	directories.append({'name': 'Unknown Fruit', 'folder':current_dir+'unknown'})
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
					for_images = cv2.resize(images, img_file_size)
					X.append(extract_features(for_images))
					y.append(index)
					print_.append(f"{filename} is an image file of type {filetype}")
				else:
					print_.append(f"{filename} is not an image file")
	X_train = np.array(X)
	y_train = np.array(y)

	X = []
	filepath = current_dir + '\\rotten\\durian\\Durian_20230419113006.png'
	images = cv2.imread(filepath)
	for_images = cv2.resize(images, img_file_size)
	X.append(extract_features(for_images))

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
@svm_algo.route('/svm/save_model', methods=['GET', 'POST'])
def svm_save_model():
	save_model()

def save_model():
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
					for_images = cv2.resize(images, img_file_size)
					X.append(extract_features(for_images))
					y.append(index)
	X_train = np.array(X)
	y_train = np.array(y)

	# # Split data into training and testing sets
	# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

	# Train SVM model
	clf = svm.SVC(kernel='linear',probability=True)
	clf.fit(X_train, y_train)

	joblib.dump(clf, 'svm_model.joblib')
def get_model():
	# Load data
	current_dir = os.getcwd()
	current_dir += '\\website\\static\\upload\\'

	X = []
	y = []

	datasets = db.session.query(Datasets.ds_name, Datasets.ds_grade).group_by(Datasets.ds_name, Datasets.ds_grade).all()
	directories = [{'name': ds_grade + ' ' + ds_name , 'folder' : current_dir+ds_grade+'\\'+ds_name.lower()} for ds_name, ds_grade in datasets]
	directories.append({'name': 'Unknown Fruit', 'folder':current_dir+'unknown'})
	print_ = []
	for index,folder in enumerate(directories):
		# print(f"Images in {folder['name']}:")
		directory = folder['folder']
		for filename in os.listdir(directory):
			filepath = os.path.join(directory, filename)
			if os.path.isfile(filepath):
				filetype = imghdr.what(filepath)
				if filetype:
					images = cv2.imread(filepath)
					for_images = cv2.resize(images, img_file_size)
					X.append(extract_features(for_images))
					y.append(index)
	X_train = np.array(X)
	y_train = np.array(y)

	# Train SVM model
	clf = svm.SVC(kernel='linear',probability=True)
	clf.fit(X_train, y_train)
	return clf,directories
def get_model_joblib():
	# Load data
	current_dir = os.getcwd()
	current_dir += '\\website\\static\\upload\\'

	X = []
	y = []

	datasets = db.session.query(Datasets.ds_name, Datasets.ds_grade).group_by(Datasets.ds_name, Datasets.ds_grade).all()
	directories = [{'name': ds_grade + ' ' + ds_name , 'folder' : current_dir+ds_grade+'\\'+ds_name.lower()} for ds_name, ds_grade in datasets]

	# Train SVM model
	clf = svm.SVC(kernel='linear',probability=True)
	clf = joblib.load('svm_model.joblib')

	return clf,directories

@svm_algo.route('/svm/detect', methods=['GET', 'POST'])
def svm_detects():
    if request.method == "POST":
        cv_image = request.files["image"]
        file_data = cv_image.read()
        nparr = np.fromstring(file_data,np.uint8)
        images = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        for_images = cv2.resize(images, img_file_size)

        X = []
        X.append(extract_features(for_images))
        X_test = np.array(X)
        result = detect_results(X_test)

        _, buffer = cv2.imencode('.jpg', images)
        img_str = base64.b64encode(buffer).decode()
        if result != "Unknown Fruit":
        	ScannedFruits.add_new_fruit(scan_img=img_str, fruit_grade=result, user_id=current_user.id)

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
    	user_id = request.form.get('user_id')
    	byte_str = base64.b64decode(img_file)
    	np_data = np.frombuffer(byte_str,dtype=np.uint8)
    	images = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

    	for_images = cv2.resize(images, img_file_size)
    	X = []
    	X.append(extract_features(for_images))
    	X_test = np.array(X)
    	result = detect_results(X_test)
    	_, buffer = cv2.imencode('.jpg', images)
    	img_str = base64.b64encode(buffer).decode()
    	print(f"Predicted: {result}")
    	if result != "Unknown Fruit":
    		ScannedFruits.add_new_fruit(scan_img=img_str, fruit_grade=result, user_id=user_id)
    	return jsonify({
    		"result":{
    			"freshness_percentage": result
    		}
    	})
    return ''
def detect_results(X_test):
	clf,directories = get_model()
	y_pred = clf.predict(X_test)
	y_prob = clf.predict_proba(X_test)
	if directories[y_pred[0]]['name'] == "Unknown Fruit":
		return "Unknown Fruit"
	for i in range(len(X_test)):
		result = directories[y_pred[0]]['name'] + ' - {:.2f}%'.format(y_prob[i][clf.predict([X_test[i]])[0]] * 100)
	return result

def predict_results(X_test,clf,directories):
	y_pred = clf.predict(X_test)
	y_prob = clf.predict_proba(X_test)
	if directories[y_pred[0]]['name'] == "Unknown Fruit":
		return "Unknown Fruit"
	for i in range(len(X_test)):
		result = directories[y_pred[0]]['name'] + ' - {:.2f}%'.format(y_prob[i][clf.predict([X_test[i]])[0]] * 100)
	return result

def imdecode_image(image_file):
    return cv2.imdecode(
        np.frombuffer(image_file.read(), np.uint8),
        cv2.IMREAD_UNCHANGED
    )

def generate_frames(clf, directories):
	cap = cv2.VideoCapture(0)
	while True:
		result = ""
		ret, frame = cap.read()

		for_images = cv2.resize(frame, (100, 100))
		X = []
		X.append(cv2.cvtColor(for_images, cv2.COLOR_BGR2GRAY).flatten())
		X_test = np.array(X)
		result = predict_results(X_test,clf,directories)

		# # Convert image to grayscale
		# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# # Apply a threshold to the image
		# thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)[1]
		# # Find contours in the thresholded image
		# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		# # Iterate through the contours
		# for contour in contours:
		# 	# Filter out small contours
		# 	if cv2.contourArea(contour) < 100:
		# 		continue
		# 	# Compute area and perimeter of contour
		# 	area = cv2.contourArea(contour)
		# 	perimeter = cv2.arcLength(contour, True)
		# 	# Compute circularity of contour
		# 	circularity = 4*np.pi*area/(perimeter**2)
		# 	# If circularity is below threshold, draw bounding box on image
		# 	if circularity < 0.5:
		# 		x, y, w, h = cv2.boundingRect(contour)
		# 		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
		cv2.rectangle(frame, (0,0), (300, 40), (245, 117, 16), -1)
		cv2.putText(frame,"Output: - " + result, (3,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

		ret,buffer=cv2.imencode('.jpg',frame)
		frame=buffer.tobytes()

		yield(b'--frame\r\n'
		       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
	cap.release()

@svm_algo.route('/video', methods=['GET', 'POST'])
def svm_video():
	clf,directories = get_model()
	return Response(generate_frames(clf,directories),mimetype='multipart/x-mixed-replace; boundary=frame')

@svm_algo.route('/live', methods=['GET', 'POST'])
def svm_live():
    return render_template("video.html")

@svm_algo.route('/api/scanned_fruits', methods=['GET','POST'])
def get_scanned_fruits():
	if request.method == "POST":
		user_id = request.form.get('user_id')
		results = ScannedFruits.get_scanned_fruits_with_user_fullname(user_id)
		scanned_fruits = []
		for scanned_fruit, fname, mname, lname in results:
			scanned_fruit_data = {
				"scan_id": scanned_fruit.scan_id,
				"scan_img": scanned_fruit.scan_img,
				"fruit_grade": scanned_fruit.fruit_grade,
				"date_added": scanned_fruit.date_added,
				"user_id": scanned_fruit.user_id,
				"user_fullname": f"{fname} {mname} {lname}"
			}
			scanned_fruits.append(scanned_fruit_data)
		return jsonify(scanned_fruits)
	return jsonify([])

@svm_algo.route('/api/delete_scanned_fruits', methods=['GET','POST'])
def delete_scanned_fruits():
	if request.method == "POST":
		user_id = request.form.get('user_id')
		scan_ids = request.form.get('scan_ids')
		for scan_id in scan_ids:
			ScannedFruits.delete_scanned_fruit(scan_id)
		return jsonify({"deleted": True})
	return jsonify(scan_ids)
@svm_algo.route('/live-detect', methods=['GET', 'POST'])
def detects2():
	clf,directories = get_model()
	last_result = ""
	cap=cv2.VideoCapture(0)
	while True:
		# Read the frame from the capture
		ret, frame = cap.read()

		if frame is not None:
			# Show the frame
			result = process_frame(frame,clf,directories,last_result)
			print("Last:"+last_result+" Current:"+result)
			last_result = result
			if cv2.waitKey(1) == ord("q"):
				break
		else:
			cap.release()
			cv2.destroyAllWindows()
			flash('Please check your camera connection!', category='error')
			return redirect(url_for('detect.detects'))
	# Release the capture and destroy the windows
	cap.release()
	cv2.destroyAllWindows()
	return redirect(url_for('detect.detects'))

def process_frame(frame,clf,directories,last_result):
	for_images = cv2.resize(frame, img_file_size)
	X = []
	X.append(extract_features(for_images))
	X_test = np.array(X)
	result = predict_results(X_test,clf,directories)
	_, buffer = cv2.imencode('.jpg', frame)
	img_str = base64.b64encode(buffer).decode()

	if result != "Unknown Fruit":
		if sameLastResult(last_result,result) != True:
			ScannedFruits.add_new_fruit(scan_img=img_str, fruit_grade=result, user_id=current_user.id)
	# cv2.putText(frame,result,(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
	cv2.rectangle(frame, (0,0), (650, 40), (245, 117, 16), -1)
	cv2.putText(frame,result, (3,30),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
	cv2.imshow(window_name,frame)
	cv2.setWindowProperty(window_name,cv2.WND_PROP_TOPMOST,1)
	return result
def process_frame_contours(frame,clf,directories,last_result):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply image preprocessing (Gaussian blur and thresholding)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate over each contour and draw a bounding box around it
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        fruit_img = frame[y:y + h, x:x + w]
        for_images = cv2.resize(fruit_img, img_file_size)
        X = []
        X.append(extract_features(for_images))
        X_test = np.array(X)
        result = predict_results(X_test,clf,directories)
        _, buffer = cv2.imencode('.jpg', frame)
        img_str = base64.b64encode(buffer).decode()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, result, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow(window_name,frame)
    cv2.setWindowProperty(window_name,cv2.WND_PROP_TOPMOST,1)
    return result
def sameLastResult(last,current):
	exploded_last = last.split()
	exploded_current = current.split()
	new_last = exploded_last[0] + " " + exploded_last[1]
	new_current = exploded_current[0] + " " + exploded_current[1]
	return new_current == new_last