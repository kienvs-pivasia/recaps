from ..model import User
from flask import request, g, jsonify, render_template, redirect, url_for
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    JWTManager
)

def register_user_service():
    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]
        response = None
        
        if response is None:
            user = g.dbsession.query(User).filter(username=username).first()
            if user:
                response = "Username is already exist"
            else:
                try:
                    newUser = User(username=username, password=password)
                    g.dbsession.add(newUser)
                    g.dbsession.commit()
                    g.dbsession.close()
                    return redirect(url_for("user.login_user"))
                except IndentationError:
                    response = "Cannot register"

        return response
    
def login_user_service():
    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]
        response = None

        if username and password:
            user = g.dbsession.query(User).filter(username=username).first()

            if user is None or user.password != password:
                response = "Incorrect username or password"
            else:
                try:
                    access_token = create_access_token(identity=username)
                    response = "Success"
                    set_access_cookies(response, access_token)
                    return response
                except IndentationError:
                    response = "Cannot login"

        return response
    
def log_out_service():
    response = redirect(url_for("user.login_user"))
    unset_jwt_cookies(response)
    return response