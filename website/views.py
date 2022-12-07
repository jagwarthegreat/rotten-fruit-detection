from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
import json
from werkzeug.utils import secure_filename
import os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return jsonify({ "result": "this is home" })
    # return render_template("home.html", user=current_user)

@views.route('/detect', methods=['GET','POST'])
def detect():
    # requestData = json.loads(request.data)
    # requestID = requestData['docId'] 
    # docdata = Document.query.get(requestID)
    # rmessage = "";
    # ctStatus = "";

    # if os.path.exists(docdata.doc_file):
    #     test = os.remove(docdata.doc_file)
    #     db.session.delete(docdata)
    #     db.session.commit()
    #     rmessage = "Deleted";
    #     ctStatus = "success"
    # else:
    #     rmessage = "not exist";
    #     ctStatus = "error"

    # flash('Document '+rmessage+'!', category=ctStatus)
    return jsonify({ "result": "test detection result" })