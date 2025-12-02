from flask import Blueprint, request, jsonify, render_template, redirect, url_for,make_response
from models.models import  Shipment, User
from models.database import Session
from .userController import get_current_user

shipments_bp = Blueprint("shipments", __name__)

@shipments_bp.route("/add_shipments", methods=["GET", "POST"])
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

        if not all([email_sender, email_receiver, pickup_lat, pickup_lng, delivery_lat, delivery_lng]):
            error = "Wszystkie pola są wymagane!"
            return render_template("add_shipments.html", error=error)

        sender = session.query(User).filter_by(email=email_sender).first()
        receiver = session.query(User).filter_by(email=email_receiver).first()

        if not sender or not receiver:
            error = "Nie znaleziono użytkownika!"
            return render_template("add_shipments.html", error=error)

        shipment = Shipment(
            user_sender=sender.id,
            user_receiver=receiver.id,
            pickup_lat=float(pickup_lat),
            pickup_lng=float(pickup_lng),
            delivery_lat=float(delivery_lat),
            delivery_lng=float(delivery_lng)
        )

        session.add(shipment)
        session.commit()
        session.close()

        return redirect(url_for("show_views.overview"))

    return render_template("add_shipments.html")

@shipments_bp.route("/follow_selected_delivery", methods=["GET", "POST"])
def follow_selected_delivery():
    with Session() as session:
        current_id_user=get_current_user()

        shipments = session.query(Shipment).filter(
            Shipment.user_sender == current_id_user,
            Shipment.status == "waiting"
        ).all()
        
        return render_template("shipment_list.html", shipments=shipments)


@shipments_bp.route("/show_map" , methods=["GET", "POST"])
def show_map():
    return render_template("show_map.html")