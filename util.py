from PIL import Image
from flask import Flask
from werkzeug.datastructures import FileStorage
import logging

class Util:
    status_response = {
        'CREATED': 201,
        'BAD_REQUEST': 400,
        'NOT_FOUND': 404,
        'DUPLICATED': 409
    }

    logging.basicConfig(filename='access.log', level=logging.DEBUG, \
        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    @staticmethod
    def remove_image_exif(img: FileStorage):
        image = Image.open(img)
        return image

    @staticmethod
    def allowed_file(filename: str):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() \
                   in ( 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' )

    @staticmethod
    def is_image(filename: str):
        return filename.split('.')[1] in ( 'png', 'jpg', 'jpeg', 'gif' )

    @staticmethod
    def create_app():
        app = Flask(__name__)
        app.config['UPLOAD_FOLDER'] = './files'
        app.add_url_rule(
            "/<file>", endpoint="serve_files", build_only=True
        )
        return app
