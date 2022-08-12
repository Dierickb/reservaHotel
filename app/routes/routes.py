from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
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
    #user_new no es objeto sino tupla (?)
    user_new = users_controller.validateLogin(user)
    #user new debería retornar el rol.
    rol = "Admin" #user_new[3]
    if check_password_hash(user_new[1],user.password):
        #la autenticación se puede realizar mediante variables de session
        session['rol'] = rol
        if rol == 'Admin':
            return redirect(url_for('api.admin'))
        elif rol == 'SuperAdmin':
            return redirect(url_for('api.admin'))
        elif rol == 'Cliente':
            return redirect(url_for('api.admin'))
    else:
        #El usuario se equivocó de contraseña
        return render_template("register/signin.html", nav=nav)
 

@global_scope.route("/signup", methods=['GET'])
def signupGet():
    form = SignUpForm
    parameters = {
        "title": "Sign-up",
        "description": "In this page the users gonna be registered"
    }
    return render_template("register/signup.html", nav=nav, **parameters, form=form)


@global_scope.route("/signup", methods=['POST'])
def signupPost():
    data = request.form
    user = User(email=data["email"], password=generate_password_hash(data["password"]),
                fullName=data["fullName"], phone=data["phone"],
                address=data["address"],rol="Cliente")

    user_new = users_controller.create(user)
    return jsonify(user_new)


@global_scope.route("/users", methods=['GET'])
def getUsers():
    users_list = users_controller.lists()

    users_dict = [user._asdict() for user in users_list]

    return jsonify(users_dict)

@global_scope.route("/admin", methods=['GET'])
def admin():
    if 'rol' in session and session['rol'] == 'Admin':
        return render_template("admin.html", nav=nav)
    else:
        return redirect(url_for('api.loginGet'))

@global_scope.route("/admin/gUser", methods=['GET'])
def gUser():
    if 'rol' in session and session['rol'] == 'Admin':
        return render_template("admin.html", nav=nav)
    else:
        return redirect(url_for('api.loginGet'))

@global_scope.route("/admin/gRooms", methods=['GET'])
def gRooms():
    if 'rol' in session and session['rol'] == 'Admin':
        return render_template("admin.html", nav=nav)
    else:
        return redirect(url_for('api.loginGet'))

@global_scope.route("/admin/gComments", methods=['GET'])
def gComments():
    if 'rol' in session and session['rol'] == 'Admin':
        return render_template("admin.html", nav=nav)
    else:
        return redirect(url_for('api.loginGet'))

@global_scope.route("/admin/gReservation", methods=['GET'])
def gReservation():
    if 'rol' in session and session['rol'] == 'Admin':
        return render_template("admin.html", nav=nav)
    else:
        return redirect(url_for('api.loginGet'))

@global_scope.route('/<rol>/logout')
def logout(rol):
    session.pop('rol', None)
    return redirect(url_for('api.loginGet'))