from flask import Blueprint, render_template
from models import AuditLog

audit_bp = Blueprint("audit", __name__)

@audit_bp.route("/audit-logs")
def audit_logs():

    logs = AuditLog.query.order_by(
        AuditLog.timestamp.desc()
    ).all()

    return render_template(
        "audit_logs.html",
        logs=logs
    )