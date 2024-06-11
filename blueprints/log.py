from flask import Blueprint, render_template, request, redirect, session
from model.models import db, LogTemperature, LogHumidity, LogActuator, LogVibration
from datetime import datetime, timedelta

log = Blueprint( "log", __name__, static_folder="static", template_folder="view" )

@log.route("/log")
def log_blueprint():
    if not session.get("user"):
        return redirect("/login")
    return render_template("log.html")

@log.route('/read_logs', methods=['GET', 'POST'])
def read_logs():
    start_date_str = request.form['start_date']
    end_date_str = request.form['end_date']

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    logs_temp = LogTemperature.query.filter(LogTemperature.timestamp >= start_date, LogTemperature.timestamp <= end_date).all()

    logs_hum = LogHumidity.query.filter(LogHumidity.timestamp >= start_date, LogHumidity.timestamp <= end_date).all()

    logs_vib = LogVibration.query.filter(LogVibration.timestamp >= start_date, LogVibration.timestamp <= end_date).all()

    log_actuator = LogActuator.query.filter(LogActuator.timestamp >= start_date, LogActuator.timestamp <= end_date).all()

    return render_template('log.html', sensor_data_temp=logs_temp, sensor_data_hum=logs_hum, log_vib=logs_vib, actuator_data=log_actuator, is_admin=session.get("role") == "admin", is_statistician=session.get("role") == "statistician", is_operator=session.get("role") == "operator")

@log.route('/delete_log_temp/<int:log_id>', methods=['POST'])
def delete_logs(log_id):
    log = LogTemperature.query.filter_by(id=log_id).first()
    db.session.delete(log)
    db.session.commit()
    return redirect('/log')

@log.route('/delete_log_hum/<int:log_id>', methods=['POST'])
def delete_logs_hum(log_id):
    log = LogHumidity.query.filter_by(id=log_id).first()
    db.session.delete(log)
    db.session.commit()
    return redirect('/log')

@log.route('/delete_log_vib/<int:log_id>', methods=['POST'])
def delete_logs_vib(log_id):
    log = LogVibration.query.filter_by(id=log_id).first()
    db.session.delete(log)
    db.session.commit()
    return redirect('/log')

@log.route('/delete_log_actuator/<int:log_id>', methods=['POST'])
def delete_logs_actuator(log_id):
    log = LogActuator.query.filter_by(id=log_id).first()
    db.session.delete(log)
    db.session.commit()
    return redirect('/log')