from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from models.models import Base, Shipment, User
import os
import flask_login
from controllers.shipmentController import shipments_bp
from controllers.userController import user_bp
from controllers.showViewsController import show_views_bp
from middlewear.middlewear import register_middlewear
from models.database import engine
import random

app = Flask(__name__)

Base.metadata.create_all(engine)

register_middlewear(app)

app.register_blueprint(shipments_bp)

app.register_blueprint(user_bp)

app.register_blueprint(show_views_bp)


if __name__ == "__main__":
    app.run(
            host='localhost',
            debug=True,
            ssl_context=('certyficats/cert.pem', 'certyficats/key.pem')
        )
