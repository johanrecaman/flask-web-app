from flask import Blueprint, render_template, session, redirect, request, Response, jsonify
import paho.mqtt.client as mqtt
import threading
import requests
from datetime import date
from model.models import db, LogTemperature, LogHumidity, LogActuator, LogVibration

from model.models import db, Sensor, Actuator
from blueprints.sensor import read_sensors
from blueprints.actuator import read_actuators
from blueprints.user import is_admin, is_statistician, is_operator 

kits = Blueprint("kits", __name__, static_folder="static", template_folder="view")

values = {"Temperature": None, "Humidity": None, "Vibration": None}
messages = []

def on_message(client, userdata, message):
    requests.post("http://127.0.0.1:8080/message-webhook", data=message.payload.decode())

@kits.route("/message-webhook", methods=["POST"])
def message_webhook():
    global values

    old_temperature = values["Temperature"]
    old_humidity = values["Humidity"]
    old_vibration = values["Vibration"]
    
    payload = request.data.decode()
    if "Temperature" in payload:
        if old_temperature != payload:
            values["Temperature"] = payload
            messages.insert(0, payload)

            temp = float(payload.split(":")[1])
            name = payload.split(":")[0]
            if temp < 10:
                temp_log = LogTemperature(name=name, value=temp, timestamp=date.today())
                db.session.add(temp_log)
                db.session.commit()

    elif "Humidity" in payload:
        if old_humidity != payload: 
            values["Humidity"] = payload
            messages.insert(0, payload)

            name = payload.split(":")[0]
            humidity = float(payload.split(":")[1])
            if humidity > 50:
                hum_log = LogHumidity(name=name,value=humidity, timestamp=date.today())
                db.session.add(hum_log)
                db.session.commit()
    elif "Vibration" in payload:
        if old_vibration != payload:
            values["Vibration"] = payload
            messages.insert(0, payload)

            name = payload.split(":")[0]
            vibration = float(payload.split(":")[1])
            if vibration > 1:
                vib_log = LogVibration(name=name,value=vibration, timestamp=date.today())
                db.session.add(vib_log)
                db.session.commit()

    return render_template("kits.html", values = values, messages=messages, is_admin=is_admin(), is_statistician=is_statistician(), is_operator=is_operator())

client = mqtt.Client()
client.on_message = on_message
client.connect("broker.mqttdashboard.com")
client.subscribe("flask-web-app-send")
threading.Thread(target=client.loop_forever).start()

@kits.route("/kits", methods=["GET", "POST"])
def kits_blueprint():
    if request.method == "POST":
        command = request.form["command"]
        client.publish("flask-web-app-receive", command)
        return redirect("/")

    if "user" not in session:
        return redirect("/login")

    return render_template("kits.html", values = values, messages=messages, is_admin=is_admin(),is_statistician=is_statistician(), is_operator=is_operator(), sensors = read_sensors(), actuators = read_actuators())


@kits.route("create_kit", methods=["POST"])
def create_kit():
    if not is_admin():
        session.clear()
        return redirect("/home")
    name = request.form.get("name")
    value = request.form.get("value")
    type = request.form.get("type")

    if type == "Sensor":
        new_kit = Sensor(name = name, value = value, type = type)
    else:
        new_kit = Actuator(name = name, value = value, type = type)
    db.session.add(new_kit)
    db.session.commit()

    return redirect("/kits")
