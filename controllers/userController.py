from flask import Blueprint, request, render_template, redirect, url_for, make_response
from models.models import  User
from models.database import Session
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timezone , timedelta 

user_bp = Blueprint("user", __name__)

SECRET = "tajny_klucz_jwt"

@user_bp.route("/register", methods=["GET", "POST"])
def register():   
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with Session() as session:
            if session.query(User).filter_by(email=email).first():
                return render_template("register.html", error="Użytkownik już istnieje")

            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password=hashed_password)

            session.add(new_user)
            session.commit()  

            token = jwt.encode({
                "user_id": new_user.id,
                "exp": datetime.now(timezone.utc) + datetime.timedelta(hours=1)
            }, SECRET, algorithm="HS256")

            resp = make_response(redirect(url_for("show_views.authorized")))
            resp.set_cookie(
                "auth", token,
                httponly=True,
                secure=False,      
                samesite="Strict"
            )

            return resp

    return render_template("register.html")

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with Session() as session:
            user = session.query(User).filter_by(email=email).first()

            if not user or not check_password_hash(user.password, password):
                return render_template("login.html", error="Nieprawidłowy email lub hasło")

            token = jwt.encode({
                "user_id": user.id,
                "exp": datetime.now(timezone.utc) + timedelta(hours=1)
            }, SECRET, algorithm="HS256")

            resp = make_response(redirect(url_for("show_views.authorized")))
            resp.set_cookie(
                "auth", token,
                httponly=True,
                secure=False,
                samesite="Strict"
            )

            return resp

    return render_template("login.html")
