from flask import Flask, render_template, request, redirect, url_for,render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, Shipment, User
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import flask_login
from controllers.shipmentController import shipments_bp
from controllers.userController import user_bp
from models.database import engine,Session

app = Flask(__name__)

Base.metadata.create_all(engine)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/authorized", methods=["GET"])
def authorized():
    return render_template("authorized.html")

app.register_blueprint(shipments_bp)

app.register_blueprint(user_bp)

@app.route("/overview")
def overview():
    with Session() as session:
        users = session.query(User).all()
        shipments = session.query(Shipment).all()
    return render_template("overview.html", users=users, shipments=shipments)


if __name__ == "__main__":
    app.run(debug=True)
