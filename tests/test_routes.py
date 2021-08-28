from io import BufferedReader
from flask import Flask
import os
import pytest
import io
from ..util import Util
# from routes import serve_files, receive_files

files_dir = 'files'
url = 'http://localhost:5000/'
image_path: str

app = Util.create_app()
from ..routes import serve_files, receive_files
# @pytest.fixture
# def app():
    # app = Util.create_app()
    # app.testing = True
    # return app
@pytest.fixture
def load_file():
    image_path = os.path.join(os.environ['PYTEST_CURRENT_TEST'].split('::')[0], os.getcwd())
    return open(f'{image_path}/tests/coffee.jpg', 'rb')


def test_create_files_directory(tmp_path):
    d = tmp_path / files_dir
    env = os.environ
    d.mkdir()

def test_receive_files(load_file):
    file = load_file
    file = (io.BytesIO(file.read()), 'coffee.jpg')
    # app: Flask = Util.create_app()
    client = app.test_client()
    response = client.post('/',
        content_type='multipart/form-data',
        data={'file': file}
    )
    assert response.status_code == 201