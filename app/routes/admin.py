from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from ..models.models import Login, Date, User, SignUpForm
from ..models.exceptions import UserAlreadyExists, UserNotFound
from werkzeug.security import generate_password_hash, check_password_hash
from ..controller import users_controller

admin_scope = Blueprint("admin", __name__)

@admin_scope.route("/", methods=['GET'])
def admin():
    if 'rol' in session and session['rol'] == 'admin':
        users_list = users_controller.lists()
        users_dict = [user._asdict() for user in users_list]

        return render_template("/admin/admin.html", users=users_dict, url=session['rol'])
    else:
        return redirect(url_for('api.loginGet'))


@admin_scope.route("/register", methods=['POST'])
def rUser():
    try:
        if 'rol' in session and session['rol'] == 'admin':
            data = request.form
            user = User(email=data["email"], password=generate_password_hash(data["password"]),
                    fullName=data["fullName"], phone=data["phone"],
                    address=data["address"], rol=data["rol"]) 
            user_new = users_controller.create(user)
            flash("Succesfully added")
            return redirect(url_for('admin.admin'))
        else:
            return redirect(url_for('api.loginGet'))
    except UserAlreadyExists as err:
        flash(err.__str__())
        return redirect(url_for('admin.admin'))


@admin_scope.route("/edit_user/<user_id>", methods=['GET'])
def edit_user(user_id):
    if 'rol' in session and session['rol'] == 'admin':
        user = users_controller.details(user_id)
        return jsonify(user)
    else:
        return redirect(url_for('api.loginGet'))


@admin_scope.route("/delete_user/<user_id>", methods=['GET'])
def delete_user(user_id):
    try:
        if 'rol' in session and session['rol'] == 'admin':
            user = users_controller.details(user_id)
            users_controller.delete(user)
            return redirect(url_for('admin.admin'))
        else:
            return redirect(url_for('api.loginGet'))
    except UserNotFound as err:
        flash(err.__str__())
        return redirect(url_for('admin.admin'))
    

