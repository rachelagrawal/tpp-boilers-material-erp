from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)

from werkzeug.security import generate_password_hash

from extensions import db

from models import User

from utils.auth import require_role

users_bp = Blueprint("users", __name__)


@users_bp.route("/users")
def users():

    require_role("Admin")

    all_users = User.query.all()

    return render_template(
        "users.html",
        users=all_users
    )


@users_bp.route("/add-user", methods=["GET", "POST"])
def add_user():

    require_role("Admin")

    if request.method == "POST":

        user = User(

            username=request.form["username"],

            password=generate_password_hash(
                request.form["password"]
            ),

            role=request.form["role"]

        )

        db.session.add(user)

        db.session.commit()

        return redirect("/users")

    return render_template("add_user.html")

@users_bp.route("/edit-user/<int:id>", methods=["GET", "POST"])
def edit_user(id):

    require_role("Admin")

    user = User.query.get_or_404(id)

    if request.method == "POST":

        user.username = request.form["username"]

        user.role = request.form["role"]

        db.session.commit()

        return redirect("/users")

    return render_template(
        "edit_user.html",
        user=user
    )

@users_bp.route("/delete-user/<int:id>")
def delete_user(id):

    require_role("Admin")

    user = User.query.get_or_404(id)

    # Don't allow deleting yourself
    if user.username == session["user"]:

        flash("You cannot delete your own account.", "danger")

        return redirect("/users")

    # Don't allow deleting the last Admin
    if user.role == "Admin":

        admin_count = User.query.filter_by(role="Admin").count()

        if admin_count <= 1:

            flash("Cannot delete the last Admin.", "danger")

            return redirect("/users")

    db.session.delete(user)

    db.session.commit()

    flash("User deleted successfully.", "success")

    return redirect("/users")