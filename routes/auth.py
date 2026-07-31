from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

from werkzeug.security import check_password_hash
from models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            return redirect("/dashboard")

    return render_template("login.html")


@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/login")