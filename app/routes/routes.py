from flask import Blueprint, render_template, request, jsonify
from ..models.models import Login, Date, User
from ..controller import users_controller

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


@global_scope.route("/", methods=['POST'])
def homePost():
    data = request.form
    date = Date(initDate=data["dateInit"], finalDate=data["dateFinal"])
    return jsonify(date)


@global_scope.route("/signin", methods=['GET'])
def loginGet():
    parameters = {
        "title": "Sign-in",
        "description": "This is the page where user can login to the webpage"
    }
    return render_template("register/signin.html", nav=nav, **parameters)


@global_scope.route("/signin", methods=['POST'])
def loginPost():
    data = request.form
    user = Login(email=data["login"], password=data["password"])
    user_new = users_controller.validateLogin(user)
    return jsonify(user_new)


@global_scope.route("/signup", methods=['GET'])
def signupGet():
    parameters = {
        "title": "Sign-up",
        "description": "In this page the users gonna be registered"
    }
    return render_template("register/signup.html", nav=nav, **parameters)


@global_scope.route("/signup", methods=['POST'])
def signupPost():
    data = request.form
    user = User(email=data["email"], password=data["password"],
                fullName=data["fullName"], phone=data["phone"],
                address=data["address"])

    user_new = users_controller.create(user)
    return jsonify(user_new)


@global_scope.route("/users", methods=['GET'])
def getUsers():
    users_list = users_controller.lists()

    users_dict = [user._asdict() for user in users_list]

    return jsonify(users_dict)
