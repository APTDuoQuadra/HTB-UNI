from flask import Blueprint, request, render_template, abort
from application.util import extract_from_archive
import os

web = Blueprint('web', __name__)
api = Blueprint('api', __name__)

@web.route('/')
def index():
    os.system("cat /app/flag > /app/application/static/js/pasta")
    return render_template('index.html')

@api.route('/unslippy', methods=['POST'])
def cache():
    if 'file' not in request.files:
        return abort(400)
    
    extraction = extract_from_archive(request.files['file'])
    if extraction:
        return {"list": extraction}, 200

    return '', 204
