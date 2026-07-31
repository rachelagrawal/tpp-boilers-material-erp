from flask import session, abort
from models import User

def current_user():

    if "username" not in session:
        return None

    return User.query.filter_by(
        username=session["username"]
    ).first()


def require_role(*roles):

    user = current_user()

    if user is None:

        abort(403)

    if user.role not in roles:

        abort(403)