from flask import Blueprint, render_template, session, redirect, request, Response, jsonify

home = Blueprint("home", __name__, static_folder="static", template_folder="view")

@home.route("/")
@home.route("/home")
def home_blueprint():
    return render_template("home.html")