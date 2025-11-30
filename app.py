from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from models.models import Base, Shipment, User
import os
import flask_login
from controllers.shipmentController import shipments_bp
from controllers.userController import user_bp
from controllers.showViewsController import show_views_bp
from models.database import engine

app = Flask(__name__)

Base.metadata.create_all(engine)

app.register_blueprint(shipments_bp)

app.register_blueprint(user_bp)

app.register_blueprint(show_views_bp)

if __name__ == "__main__":
    app.run(debug=True)
