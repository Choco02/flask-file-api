from flask import jsonify, send_from_directory, request, url_for, Blueprint
from werkzeug.utils import secure_filename
from .util import Util
import os, sys

serve_files_route = Blueprint('serve_files_route', '__main__')
receive_files_route = Blueprint('receive_files_route', '__main__')

files_folder = './files'

@serve_files_route.route('/<file>')
def serve_files(file):
    if request.method not in ['GET', 'POST']:
        return jsonify({ 'message': 'Method not allowed' }), \
            Util.status_response['METHOD_NOT_ALLOWED']

    if file not in os.listdir(files_folder):
        return jsonify({ 'message': 'File Not Found' }), \
             Util.status_response['NOT_FOUND']
    
    return send_from_directory(f'.{files_folder}', file, environ=request.environ)

@receive_files_route.route('/', methods=['POST'])
def receive_files():
    if request.method not in ['GET', 'POST']:
        return jsonify({ 'message': 'Method not allowed' }), \
            Util.status_response['METHOD_NOT_ALLOWED']

    if 'file' not in request.files:
        return jsonify({ 'message': 'No files were sent' }), \
            Util.status_response['BAD_REQUEST']

    file = request.files['file']
    if not file.filename:
        return jsonify({ 'message': 'File without name' }), \
        Util.status_response['BAD_REQUEST']

    if file and Util.allowed_file(file.filename):
        filename = secure_filename(file.filename)

        if filename in os.listdir(files_folder):
            return jsonify({ 'message': 'File already exists' }), \
                Util.status_response['DUPLICATED']

        if Util.is_image(filename):
            file = Util.remove_image_exif(file)

        file.save(os.path.join(files_folder, filename))
        data = url_for('serve_files', file=filename, _external=True)
        return jsonify({ 'message': data }), Util.status_response['CREATED']
