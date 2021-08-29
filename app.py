from .util import Util
app = Util().create_app()

from .routes import serve_files_route, receive_files_route

app.register_blueprint(serve_files_route)
app.register_blueprint(receive_files_route)
