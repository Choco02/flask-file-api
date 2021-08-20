import os
from PIL import Image
from flask import Flask, request, url_for, jsonify
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename, send_from_directory
import logging

class Utils:
    def __init__(self):

        self.status_response = {
            'CREATED': 201,
            'BAD_REQUEST': 400,
            'NOT_FOUND': 404,
            'DUPLICATED': 409
        }

        self.UPLOAD_FOLDER = './files'
        self.ALLOWED_EXTENSIONS = ( 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' )

        logging.basicConfig(filename='access.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    @staticmethod
    def remove_image_exif(self, img: FileStorage):
        image = Image.open(img)
        return image

    @staticmethod
    def allowed_file(self, filename: str):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    @staticmethod
    def is_image(self, filename: str):
        filename.split('.')[1] in self.ALLOWED_EXTENSIONS[2:]

    @staticmethod
    def create_app(self):
        app = Flask(__name__)
        app.config['UPLOAD_FOLDER'] = self.UPLOAD_FOLDER
        app.add_url_rule(
            "/<file>", endpoint="serve_files", build_only=True
        )
        return app

app = Utils.create_app()

@app.route('/<file>', methods=['GET'])
def serve_files(file):
    files_folder = app.config['UPLOAD_FOLDER']
    if file not in os.listdir(files_folder):
        return jsonify({ 'message': 'File Not Found' }), Utils.status['NOT_FOUND']
    return send_from_directory(files_folder, file, environ=request.environ)


@app.route('/', methods=['POST'])
def receive_files():
    if 'file' not in request.files:
        return jsonify({ 'message': 'No files were sent' }), Utils.status['BAD_REQUEST']
    file = request.files['file']
    if not file.filename:
        return jsonify({ 'message': 'File without name' }), Utils.status['BAD_REQUEST']

    if file and Utils.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if filename in os.listdir(app.config['UPLOAD_FOLDER']):
            return jsonify({ 'message': 'File already exists' }), Utils.status['DUPLICATED']
        if Utils.is_image(filename):
            file = Utils.remove_image_exif(file)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = url_for('serve_files', file=filename, _external=True)
        return jsonify({ 'message': data }), Utils.status['BAD_REQUEST']
