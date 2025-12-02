from flask import Blueprint, request, render_template, redirect, url_for,make_response
from models.models import  User,Shipment
from models.database import Session

show_views_bp = Blueprint("show_views", __name__)

@show_views_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@show_views_bp.route("/authorized", methods=["GET"])
def authorized():
    return render_template("authorized.html")

@show_views_bp.route("/overview")
def overview():
    with Session() as session:
        users = session.query(User).all()
        shipments = session.query(Shipment).all()
    return render_template("overview.html", users=users, shipments=shipments)

@show_views_bp.route("/show_all")
def show_all():
    with Session() as session:
        users = session.query(User).all()
        shipments = session.query(Shipment).all()
    return render_template("show_all.html", users=users, shipments=shipments)

@show_views_bp.route("/logout")
def logout():
    resp = make_response(redirect(url_for("user.login")))
    resp.delete_cookie("auth")
    return resp

