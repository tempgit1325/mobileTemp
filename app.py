from flask import Flask, render_template, request, redirect, url_for,render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Shipment, User
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import flask_login

app = Flask(__name__)

# loading variables from .env file
load_dotenv() 

db=os.getenv("DATABASE")
postgres_passw=os.getenv("POSTGRES_PASSWORD")
postgres_user=os.getenv("POSTGRES_USER")

DATABASE_URL = f"postgresql+psycopg2://{postgres_user}:{postgres_passw}@localhost:5432/{db}"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  
Session = sessionmaker(bind=engine)
session = Session()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session = Session()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        

        if session.query(User).filter_by(email=email).first():
            return render_template("register.html", error="Użytkownik już istnieje")

        with Session() as session:
            if session.query(User).filter_by(email=email).first():
                return render_template("register.html", error="Użytkownik już istnieje")

            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password=hashed_password)

            session.add(new_user)
            session.commit()
        
        return redirect(url_for("authorized"))

    session.close()
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session = Session()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session.close()
            return redirect(url_for("authorized"))
        else:
            session.close()
            return render_template("login.html", error="Nieprawidłowy email lub hasło")

    session.close()
    return render_template("login.html")

@app.route("/authorized", methods=["GET"])
def authorized():
    return render_template("authorized.html")

@app.route("/add_shipments", methods=["GET", "POST"])
def add_shipments():
    session = Session()
    error = None

    if request.method == "POST":
        email_sender = request.form.get("EmailSender")
        email_receiver = request.form.get("EmailReceiver")
        pickup_lat = request.form.get("pickup_lat")
        pickup_lng = request.form.get("pickup_lng")
        delivery_lat = request.form.get("delivery_lat")
        delivery_lng = request.form.get("delivery_lng")

        # walidacja podstawowa
        if not all([email_sender, email_receiver, pickup_lat, pickup_lng, delivery_lat, delivery_lng]):
            error = "Wszystkie pola są wymagane!"
            return render_template("add_shipments.html", error=error)

        # wyszukanie userów
        sender = session.query(User).filter_by(email=email_sender).first()
        receiver = session.query(User).filter_by(email=email_receiver).first()

        if not sender or not receiver:
            error = "Nie znaleziono użytkownika o podanych emailach!"
            return render_template("add_shipments.html", error=error)

        # utworzenie przesyłki
        shipment = Shipment(
            user_sender=sender.email,
            user_receiver=receiver.email,
            pickup_lat=float(pickup_lat),
            pickup_lng=float(pickup_lng),
            delivery_lat=float(delivery_lat),
            delivery_lng=float(delivery_lng)
        )

        session.add(shipment)
        session.commit()
        session.close()

        return redirect(url_for("overwiew"))

    return render_template("add_shipments.html")

@app.route("/overwiew", methods=["GET"])
def overwiew():
    users=session.query(User).all()
    shipments = session.query(Shipment).all()
    return render_template("overview.html", users=users, shipments=shipments)

if __name__ == "__main__":
    app.run(debug=True)
