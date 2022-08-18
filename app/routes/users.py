from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from ..models.models import Login, Date, User, SignUpForm
from ..models.exceptions import UserAlreadyExists, UserNotFound
from werkzeug.security import generate_password_hash, check_password_hash
from ..controller import users_controller, rooms_controller

user_scope = Blueprint("user", __name__)

@user_scope.route("/", methods=['GET', 'POST'])
def user():
    if 'rol' in session and session['rol'] == 'user' and request.method == 'GET':
        return render_template("home.html", url=request.path)

    elif 'rol' in session and session['rol'] == 'user' and request.method == 'POST':
        data = request.form
        date = Date(initDate=data["dateInit"], finalDate=data["dateFinal"])
        flash("Ha reservado correctamente la habitacion")
        return render_template("home.html", url=request.path)
    else:
        return redirect(url_for('api.loginGet'))
   