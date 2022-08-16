from flask import Flask
from config import Config
from .database.users_db import reset_table
from .database.rooms_db import reset_room_table
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

from .routes import global_scope, admin_scope#, errors_scope

app = Flask(__name__, static_folder=Config.STATIC_FOLDER,
            template_folder=Config.TEMPLATE_FOLDER)
app.config.from_object(Config)  # Config es el nombre de la clase
csrf.init_app(app)

app.register_blueprint(global_scope, url_prefix="/")
# app.register_blueprint(errors_scope, url_prefix="/")
app.register_blueprint(admin_scope, url_prefix="/admin")

reset_table()
reset_room_table()
