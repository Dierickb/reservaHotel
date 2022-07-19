from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from ..models.models import Login

global_scope = Blueprint("api", __name__)

nav = [
    {"name": "Listar Todos", "url": "/api/contacts"},
    {"name": "Contacto ID 1", "url": "/api/contacts/1"}
]


@global_scope.route("/", methods=['GET'])
def home():
    """Landing page route."""

    parameters = {"title": "Flask and Jinja Practicial work",
                  "description": "This is a simple page made for implement"
                  }

    return render_template("home.html", nav=nav, **parameters)


@global_scope.route("/signin", methods=['GET'])
def loginGet():
    parameters = {
        "title": "Sign-in",
        "description": "This is the page where user can login to the webpage"
    }
    return render_template("signin.html", nav=nav, **parameters)


@global_scope.route("/signin", methods=['POST'])
def loginPost():
    data = request.form
    user = Login(nickName=data["login"], password=data["password"])
    return jsonify(user)