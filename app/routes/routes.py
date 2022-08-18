from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash

from ..models.exceptions import UserNotFound, UserAlreadyExists
from ..models.models import Login, Date, User, SignUpForm
from ..controller import users_controller
from werkzeug.security import generate_password_hash, check_password_hash

global_scope = Blueprint("api", __name__)

nav = [
    {"name": "Listar Todos", "url": "/api/contacts"},
    {"name": "Contacto ID 1", "url": "/api/contacts/1"}
]


@global_scope.route("/", methods=['GET'])
def home():
    """Landing page route."""

    parameters = {"title": "Home",
                  "description": "This is a simple page made for implement",
                  "url": request.path
                  }

    return render_template("home.html", **parameters)

@global_scope.route("/signin", methods=['GET'])
def loginGet():
    parameters = {
        "title": "Sign-in",
        "description": "This is the page where user can login to the webpage",
        "url": request.path
    }
    return render_template("register/signin.html", nav=nav, **parameters)


@global_scope.route("/signin", methods=['POST'])
def loginPost():
    try:
        data = request.form
        user = Login(email=data["login"], password=data["password"])
        user_new = users_controller.validateLogin(user)
        if check_password_hash(user_new.password, user.password):
            session['rol'] = user_new.rol
            if user_new.rol == 'admin':
                return redirect(url_for('admin.admin'))
            elif user_new.rol == 'superadmin':
                return redirect(url_for('admin.admin'))
            elif user_new.rol == 'user':
                return redirect(url_for('user.user'))
        else:
            flash("Check your credentials and try again")
            return render_template("register/signin.html", nav=nav, url= request.path)
    except UserNotFound as err:
        flash(err.__str__())
        return render_template("register/signin.html", nav=nav, url= request.path)


@global_scope.route("/signup", methods=['GET'])
def signupGet():
    form = SignUpForm
    parameters = {
        "title": "Sign-up",
        "description": "In this page the users gonna be registered",
        "url": request.path
    }
    return render_template("register/signup.html", nav=nav, **parameters, form=form)


@global_scope.route("/signup", methods=['POST'])
def signupPost():
    try:
        data = request.form
        user = User(email=data["email"], password=generate_password_hash(data["password"]),
                    fullName=data["fullName"], phone=data["phone"], rol="user")
        user_new = users_controller.create(user)
        return redirect(url_for('api.loginGet'))

    except UserAlreadyExists as err:
        flash(err.__str__())
        return render_template("register/signup.html", nav=nav, url= request.path)


@global_scope.route("/users", methods=['GET'])
def getUsers():
    users_list = users_controller.lists()

    users_dict = [user._asdict() for user in users_list]

    return jsonify(users_dict)


@global_scope.route('/<rol>/logout')
def logout(rol):
    session.pop('rol', None)
    return redirect(url_for('api.loginGet'))
