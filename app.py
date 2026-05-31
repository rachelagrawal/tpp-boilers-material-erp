from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
app = Flask(__name__)
app.config.from_object("config.Config")
app.secret_key = "tpp_boilers_secret"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(50)
    )

class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)

    item_code = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    material_name = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    specification = db.Column(
        db.Text
    )

    uom = db.Column(
        db.String(20)
    )

    min_stock = db.Column(
        db.Float
    )

    max_stock = db.Column(
        db.Float
    )

@app.route("/login", methods=["GET", "POST"])
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

            session["user"] = user.username

            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/")
def home():
    return "TPP Boilers ERP"

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user=session["user"]
    )

@app.route("/add-item", methods=["GET", "POST"])
def add_item():

    if request.method == "POST":

        item = Item(
            item_code=request.form["item_code"],
            material_name=request.form["material_name"],
            category=request.form["category"],
            uom=request.form["uom"]
        )

        db.session.add(item)
        db.session.commit()

        return redirect("/items")

    return render_template("add_item.html")


@app.route("/items")
def items():

    all_items = Item.query.all()

    return render_template(
        "items.html",
        items=all_items
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

    session.clear()

    return redirect("/login")


if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        if not User.query.filter_by(
            username="admin"
        ).first():

            user = User(
                username="admin",
                password=generate_password_hash(
                    "admin123"
                ),
                role="Admin"
            )

            db.session.add(user)
            db.session.commit()

    app.run(debug=True)