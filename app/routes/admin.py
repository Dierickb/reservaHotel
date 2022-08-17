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
        user = users_controller.details(0)

        return render_template("/admin/admin.html", users=users_dict, url=request.path, user=user)
    else:
        return redirect(url_for('api.loginGet'))


@admin_scope.route("/", methods=['POST'])
def rUser():
    try:
        if 'rol' in session and session['rol'] == 'admin':
            data = request.form
            user = User(email=data["email"], password=generate_password_hash(data["password"]),
                        fullName=data["fullName"], phone=data["phone"], rol=data["rol"])
            user_new = users_controller.create(user)
            flash("Successfully added")
            return redirect(url_for('admin.edit_user', user_id=user_new.id))
        else:
            return redirect(url_for('api.loginGet'))
    except UserAlreadyExists as err:
        flash(err.__str__())
        return redirect(url_for('admin.admin'))


@admin_scope.route("/select_user/<user_id>", methods=['GET'])
def get_user(user_id):
    if 'rol' in session and session['rol'] == 'admin':
        users_list = users_controller.lists()
        users_dict = [user._asdict() for user in users_list]
        user = users_controller.details(user_id)

        return render_template("/admin/admin.html", user=user,
                               url=request.path, users=users_dict)
    else:
        return redirect(url_for('api.loginGet'))


@admin_scope.route("/edit_user/<user_id>", methods=['POST', 'GET'])
def edit_user(user_id):
    print("update")
    if 'rol' in session and session['rol'] == 'admin' and request.method == 'POST':
        users_list = users_controller.lists()
        users_dict = [user._asdict() for user in users_list]

        data = request.form
        userEdited = User(id=user_id ,email=data["email"], password=generate_password_hash(data["password"]),
                    fullName=data["fullName"], phone=data["phone"], rol=data["rol"])

        new_user = users_controller.update(userEdited)

        return render_template("/admin/admin.html", user=new_user,
                               url=request.path, users=users_dict)

    elif 'rol' in session and session['rol'] == 'admin' and request.method == 'GET':
        users_list = users_controller.lists()
        users_dict = [user._asdict() for user in users_list]
        user = users_controller.details(user_id)

        return render_template("/admin/admin.html", user=user,
                               url=request.path, users=users_dict)

    else:
        return redirect(url_for('api.loginGet'))


@admin_scope.route("/delete_user/<user_id>", methods=['POST'])
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
