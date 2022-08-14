from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from ..models.models import Login, Date, User, SignUpForm
from ..controller import users_controller

admin_scope = Blueprint("admin", __name__)

@admin_scope.route("/", methods=['GET'])
def admin():
    if 'rol' in session and session['rol'] == 'Admin':
        print(request.path)
        return render_template("/admin/admin.html", rol=session['rol'], url=request.path)
    else:
        return redirect(url_for('api.loginGet'))


@admin_scope.route("/gUser", methods=['GET'])
def gUser():
    if 'rol' in session and session['rol'] == 'Admin':
        return render_template("admin.html")
    else:
        return redirect(url_for('api.loginGet'))


@admin_scope.route("/gRooms", methods=['GET'])
def gRooms():
    if 'rol' in session and session['rol'] == 'Admin':
        return render_template("admin.html")
    else:
        return redirect(url_for('api.loginGet'))


@admin_scope.route("/gComments", methods=['GET'])
def gComments():
    if 'rol' in session and session['rol'] == 'Admin':
        return render_template("admin.html")
    else:
        return redirect(url_for('api.loginGet'))


@admin_scope.route("/gReservation", methods=['GET'])
def gReservation():
    if 'rol' in session and session['rol'] == 'Admin':
        return render_template("admin.html")
    else:
        return redirect(url_for('api.loginGet'))


@admin_scope.route('/<rol>/logout')
def logout(rol):
    session.pop('rol', None)
    return redirect(url_for('api.loginGet'))
