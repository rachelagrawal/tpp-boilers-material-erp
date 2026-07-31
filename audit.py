from flask import session
from extensions import db
from models import AuditLog

def log_action(action):

    user_id = session.get("user_id")

    if not user_id:
        return

    log = AuditLog(
        user_id=user_id,
        action=action
    )

    db.session.add(log)
    db.session.commit()