from flask import Blueprint, render_template, session, redirect, request, Response, jsonify

home = Blueprint("home", __name__, static_folder="static", template_folder="view")

@home.route("/home")
def home_blueprint():
    if not session.get("user"):
        return redirect("/login")
    return render_template("home.html")