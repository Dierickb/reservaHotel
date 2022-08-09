from flask import Flask
from config import Config
from .database.users_db import reset_table
from .database.rooms_db import reset_room_table

from .routes import global_scope  # , api_scope, errors_scope

app = Flask(__name__, static_folder=Config.STATIC_FOLDER,
            template_folder=Config.TEMPLATE_FOLDER)
app.config.from_object(Config)  # Config es el nombre de la clase

app.register_blueprint(global_scope, url_prefix="/")
# app.register_blueprint(errors_scope, url_prefix="/")
# app.register_blueprint(api_scope, url_prefix="/api")

reset_table()
reset_room_table()
