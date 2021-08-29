import os
import pytest
import io

files_dir = 'files'
image_path: str

from .util import Util
from .routes import serve_files_route, receive_files_route

app = Util.create_app()

app.register_blueprint(serve_files_route)
app.register_blueprint(receive_files_route)

def get_environ():
    return os.path.join(os.environ.get('PYTEST_CURRENT_TEST')
        .split('::')[0], os.getcwd())

def load_file():
    image_path = get_environ()
    return open(f'{image_path}/tests/coffee.jpg', 'rb')

def delete_file():
    image_to_remove = get_environ()
    os.remove(f'{image_to_remove}/files/coffee.jpg')
    return 'File has been deleted'

@pytest.mark.parametrize('test_input,expected', [
        (load_file, Util.status_response['CREATED']),
        (load_file, Util.status_response['DUPLICATED'])
    ])
def test_receive_files(test_input, expected):
    # Testing file upload and duplicated file
    file = test_input()
    file = (io.BytesIO(file.read()), 'coffee.jpg')
    client = app.test_client()
    response = client.post('/',
        content_type='multipart/form-data',
        data={'file': file}
    )
    assert response.status_code == expected

@pytest.mark.parametrize('test_input,expected', [
    ('2474216.jpg', Util.status_response['OK']),
    ('coffee.jpg', Util.status_response['OK']),
    ('aaa', Util.status_response['NOT_FOUND']),
    ('delete_file', 'File has been deleted')
])
def test_serve_files(test_input, expected):
    # Testing file already uploaded
    if test_input == 'delete_file':
        assert delete_file() == expected
        return

    client = app.test_client()
    response = client.get(f'/{test_input}')

    assert response.status_code == expected
