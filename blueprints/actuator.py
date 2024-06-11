from flask import Blueprint, render_template, redirect, request, session
from blueprints.user import is_admin
from model.models import db, Actuator

actuator = Blueprint("actuator", __name__, static_folder="static", template_folder="view")

@actuator.route("/read_actuators")
def read_actuators():
    actuators = Actuator.query.all()
    return actuators

@actuator.route("/delete_actuator/<int:actuator_id>", methods=["POST"])
def delete_actuator(actuator_id):
    if not is_admin():
        session.clear()
        return redirect("/home")
    actuator = Actuator.query.filter_by(id=actuator_id).first()
    if actuator:
        db.session.delete(actuator)
        db.session.commit()
    return redirect("/kits")

