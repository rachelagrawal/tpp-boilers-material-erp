from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for
    
)
from flask_migrate import Migrate
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from extensions import db

app = Flask(__name__)
app.config.from_object("config.Config")
app.secret_key = "tpp_boilers_secret"

db.init_app(app)
migrate = Migrate(app, db)

from models import *
from routes.auth import auth
from routes.items import item_bp
app.register_blueprint(auth)
app.register_blueprint(item_bp)

from routes.suppliers import supplier_bp
app.register_blueprint(supplier_bp)

from routes.purchase_orders import po_bp
app.register_blueprint(po_bp)

from routes.inventory import inventory_bp
app.register_blueprint(inventory_bp)

from routes.grns import grn_bp
app.register_blueprint(grn_bp)

from routes.stock_issue import stock_issue_bp
app.register_blueprint(stock_issue_bp)

from routes.dashboard import dashboard_bp
app.register_blueprint(dashboard_bp)

from routes.reports import report_bp
app.register_blueprint(report_bp)

from routes.users import users_bp
app.register_blueprint(users_bp)

from routes.audit import audit_bp
app.register_blueprint(audit_bp)

from routes.inventory_history import inventory_history_bp
app.register_blueprint(inventory_history_bp)

from routes.material_return import material_return_bp
app.register_blueprint(material_return_bp)

from routes.purchase_requisitions import purchase_requisitions_bp
app.register_blueprint(purchase_requisitions_bp)

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        if not User.query.filter_by(username="admin").first():
            admin = User(
                username="admin",
                password=generate_password_hash("admin123"),
                role="Admin"
            )
            db.session.add(admin)
        if not User.query.filter_by(username="demo").first():
            demo = User(
                username="demo",
                password=generate_password_hash("demo123"),
                role="Store Manager"
            )
            db.session.add(demo)

        db.session.commit()

    app.run(debug=True)