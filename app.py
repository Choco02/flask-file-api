import os
from PIL import Image
from flask import Flask, request, url_for, jsonify
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename, send_from_directory
import logging

logging.basicConfig(filename='access.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

status = {
    'CREATED': 201,
    'BAD_REQUEST': 400,
    'NOT_FOUND': 404,
    'DUPLICATED': 409
}


UPLOAD_FOLDER = './files'
ALLOWED_EXTENSIONS = ( 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' )

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule(
    "/<file>", endpoint="serve_files", build_only=True
)

def remove_image_exif(img: FileStorage):
    image = Image.open(img)
    return image

def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/<file>', methods=['GET'])
def serve_files(file):
    files_folder = app.config['UPLOAD_FOLDER']
    if file not in os.listdir(files_folder):
        return jsonify({ 'message': 'File Not Found'}), status['NOT_FOUND']
    return send_from_directory(files_folder, file, environ=request.environ)


@app.route('/', methods=['POST'])
def receive_files():
    if 'file' not in request.files:
        return jsonify({ 'message': 'No files were sent'}), status['BAD_REQUEST']
    file = request.files['file']
    if not file.filename:
        return jsonify({ 'message': 'File without name' }), status['BAD_REQUEST']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if filename in os.listdir(app.config['UPLOAD_FOLDER']):
            return jsonify({ 'message': 'File already exists'}), status['DUPLICATED']
        if filename.split('.')[1] in ALLOWED_EXTENSIONS[2:]:
            file = remove_image_exif(file)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = url_for('serve_files', file=filename, _external=True)
        return jsonify({ 'message': data }), status['BAD_REQUEST']
