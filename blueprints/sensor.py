from flask import Blueprint, render_template, redirect, request, session
from blueprints.user import is_admin
from model.models import db, Sensor

sensor = Blueprint("sensor", __name__, static_folder="static", template_folder="view")

def read_sensors():
    sensors = Sensor.query.all()
    return sensors

@sensor.route("/delete_sensor/<int:sensor_id>", methods=["POST"])
def delete_sensor(sensor_id):
    if not is_admin():
        session.clear()
        return redirect("/home")
    sensor = Sensor.query.filter_by(id=sensor_id).first()
    if sensor:
        db.session.delete(sensor)
        db.session.commit()
    return redirect("/kits")


