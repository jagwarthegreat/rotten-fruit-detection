from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json
from werkzeug.utils import secure_filename
import os
import torch.nn as nn
import torch
import numpy as np
from torchvision import transforms
import cv2
import base64
from net import Net

detect = Blueprint('detect', __name__)
ML_MODEL = None
ML_MODEL_FILE = "model.pt"
TORCH_DEVICE = "cpu"

def get_model():
    """Loading the ML model once and returning the ML model"""
    global ML_MODEL
    if not ML_MODEL:
        ML_MODEL = Net()
        ML_MODEL.load_state_dict(
            torch.load(ML_MODEL_FILE, map_location=torch.device(TORCH_DEVICE))
        )

    return ML_MODEL

def freshness_label(freshness_percentage):
    if freshness_percentage > 90:
        return "Excellent"
    elif freshness_percentage > 65:
        return "Very Good"
    elif freshness_percentage > 50:
        return "Good"
    elif freshness_percentage > 0:
        return "Bad"
    else:
        return "Very Bad"

def price_to_text(price):
    if price == 0:
        return "Gratis"

    return str(price)

def price_by_freshness_percentage(freshness_percentage):
    return int(freshness_percentage/100*10000)

def freshness_percentage_by_cv_image(cv_image):
    """
    Reference: https://github.com/anshuls235/freshness-detector/blob/4cd289fb05a14d3c710813fca4d8d03987d656e5/main.py#L40
    """
    mean = (0.7369, 0.6360, 0.5318)
    std = (0.3281, 0.3417, 0.3704)
    transformation = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])
    image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (32, 32))
    image_tensor = transformation(image)
    batch = image_tensor.unsqueeze(0)
    out = get_model()(batch)
    s = nn.Softmax(dim=1)
    result = s(out)
    return int(result[0][0].item()*100)

def imdecode_image(image_file):
    return cv2.imdecode(
        np.frombuffer(image_file.read(), np.uint8),
        cv2.IMREAD_UNCHANGED
    )

def recognize_fruit_by_cv_image(cv_image):
    freshness_percentage = freshness_percentage_by_cv_image(cv_image)
    return {
        # TODO: change freshness_level to freshness_percentage
        "freshness_level": freshness_percentage,
        "price": price_by_freshness_percentage(freshness_percentage)
    }

@detect.route('/detect', methods=['GET', 'POST'])
def detects():
    if request.method == "POST":
        cv_image = imdecode_image(request.files["image"])
        fruit_information = recognize_fruit_by_cv_image(cv_image)
        # TODO: change freshness_level to freshness_percentage
        freshness_percentage = fruit_information["freshness_level"]

        # show submitted image
        image_content = cv2.imencode('.jpg', cv_image)[1].tobytes()
        encoded_image = base64.encodebytes(image_content)
        base64_image = 'data:image/jpg;base64, ' + str(encoded_image, 'utf-8')
        return render_template(
            "detect.html",
            display_style="display:block;",
            user=current_user,
            freshness_percentage=freshness_percentage,
            freshness_label=freshness_label(freshness_percentage),
            base64_image=base64_image,
            price=price_to_text(fruit_information["price"])
        )
    return render_template("detect.html", user=current_user,display_style="display:none;")

@detect.route('/api/detect2', methods=['GET', 'POST'])
def api_detect():
    if request.method == "POST":
        img_file = request.form.get('img_file')
        bytes_data = base64.b64decode(img_file)

        # Convert bytes to NumPy array
        np_data = np.frombuffer(bytes_data, dtype=np.uint8)

        # Convert NumPy array to cv_image object
        cv_image = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        # cv_image = imdecode_image(decoded_img_data)
        fruit_information = recognize_fruit_by_cv_image(cv_image)
        # TODO: change freshness_level to freshness_percentage
        freshness_percentage = fruit_information["freshness_level"]

        return jsonify({
            "result":{
                "freshness_percentage": freshness_percentage
            }
        })