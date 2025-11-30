from flask import Blueprint, request, render_template, redirect, url_for
from models.models import  User
from models.database import Session
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint("user", __name__)

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

        return redirect(url_for("authorized"))

    return render_template("register.html")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with Session() as session:
            user = session.query(User).filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                return redirect(url_for("authorized"))
            else:
                return render_template("login.html", error="Nieprawidłowy email lub hasło")

    return render_template("login.html")
