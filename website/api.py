from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
import json
from werkzeug.utils import secure_filename
import os

api = Blueprint('api', __name__)

@api.route('/login', methods=['GET', 'POST'])
def apiLogin():
    return jsonify({ "result": "this is api login" })
    # return render_template("home.html", user=current_user)

@api.route('/register', methods=['GET','POST'])
def apiRegister():
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

@api.route('/profile', methods=['GET', 'POST'])
def apiProfile():
    return jsonify({ "result": "this is api profile" })

@api.route('/password', methods=['GET', 'POST'])
def apiPassword():
    return jsonify({ "result": "this is api password" })