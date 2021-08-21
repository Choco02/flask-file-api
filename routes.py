from flask import jsonify, send_from_directory, request, url_for
from werkzeug.utils import secure_filename
from util import Util
from app import app
import os

@app.route('/<file>', methods=['GET'])
def serve_files(file):
    files_folder = app.config['UPLOAD_FOLDER']
    if file not in os.listdir(files_folder):
        return jsonify({ 'message': 'File Not Found' }), \
             Util.status_response['NOT_FOUND']
    
    return send_from_directory(files_folder, file, environ=request.environ)

@app.route('/', methods=['POST'])
def receive_files():
    if 'file' not in request.files:
        return jsonify({ 'message': 'No files were sent' }), \
            Util.status_response['BAD_REQUEST']

    file = request.files['file']
    if not file.filename:
        return jsonify({ 'message': 'File without name' }), \
        Util.status_response['BAD_REQUEST']

    if file and Util.allowed_file(file.filename):
        filename = secure_filename(file.filename)

        if filename in os.listdir(app.config['UPLOAD_FOLDER']):
            return jsonify({ 'message': 'File already exists' }), \
                Util.status_response['DUPLICATED']

        if Util.is_image(filename):
            file = Util.remove_image_exif(file)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = url_for('serve_files', file=filename, _external=True)
        return jsonify({ 'message': data }), Util.status_response['CREATED']
