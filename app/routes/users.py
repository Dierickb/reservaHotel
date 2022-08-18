from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from ..models.models import Login, Date, User, Room
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
        rooms_list = rooms_controller.lists()
        rooms_availables = [room for room in rooms_list if room.available == True] 
        if len(rooms_availables) > 0:
            updateRoom = Room(id=rooms_availables[0].id, 
                               location=session["id_user"], 
                               available=False
                            )
            rooms_controller.update(updateRoom)
            flash("Ha reservado correctamente la habitacion " + str(rooms_availables[0].id) + " desde " + date.initDate + " hasta " + date.finalDate )
        else:
            flash("En el momento no hay habitaciones disponibles")

        return render_template("home.html", url=request.path)
    else:
        return redirect(url_for('api.loginGet'))
   

@user_scope.route("/cancel", methods=['GET', 'POST'])
def cancel():
    if 'rol' in session and session['rol'] == 'user' and request.method == 'GET':
        rooms_list = rooms_controller.lists()
        select_room = [room for room in rooms_list if str(room.location) == session["id_user"]] 
        if len(select_room) > 0: 
            Cancelroom = Room(id=select_room[0].id, 
                                location="", 
                                available=True
                                )
            rooms_controller.update(Cancelroom)
            flash("Ha cancelado correctamente la habitacion " + str(select_room[0].id))
        else:
            flash("Usted no tiene habitaciones reservadas")

        return redirect(url_for('user.user'))
    else:
        return redirect(url_for('api.loginGet'))