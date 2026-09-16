from flask import Blueprint, render_template

user = Blueprint("user", __name__)


@user.route("/dashboard")
def dashboard():
    return render_template("user/dashboard.html")



@user.route("/profile")
def profile():
    return render_template("user/profile.html")