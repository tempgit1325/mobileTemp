from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models.models import  Shipment, User
from models.database import Session

map_bp = Blueprint("map", __name__)

@map_bp.route("/show_map", methods=["GET", "POST"])
def show_map():
    session = Session()
    error = None