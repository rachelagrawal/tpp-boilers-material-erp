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

class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)

    supplier_code = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    supplier_name = db.Column(
        db.String(150),
        nullable=False
    )

    contact_person = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(20)
    )

    email = db.Column(
        db.String(100)
    )

    gst_number = db.Column(
        db.String(30)
    )

    address = db.Column(
        db.Text
    )

class PurchaseOrder(db.Model):
    __tablename__ = "purchase_orders"

    id = db.Column(db.Integer, primary_key=True)

    po_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    supplier = db.relationship(
    "Supplier"
    )


    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("suppliers.id")
    )

    order_date = db.Column(
        db.String(20)
    )

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    total_amount = db.Column(
        db.Float,
        default=0
    )

class PurchaseOrderItem(db.Model):
    __tablename__ = "purchase_order_items"

    id = db.Column(db.Integer, primary_key=True)

    po_id = db.Column(
        db.Integer,
        db.ForeignKey("purchase_orders.id")
    )

    
    item = db.relationship(
    "Item"
    )


    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.id")
    )

    quantity = db.Column(
        db.Float
    )

    rate = db.Column(
        db.Float
    )

    line_total = db.Column(
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


@app.route(
    "/add-supplier",
    methods=["GET", "POST"]
)
def add_supplier():

    if request.method == "POST":

        supplier = Supplier(
            supplier_code=request.form["supplier_code"],
            supplier_name=request.form["supplier_name"],
            contact_person=request.form["contact_person"],
            phone=request.form["phone"],
            email=request.form["email"],
            gst_number=request.form["gst_number"],
            address=request.form["address"]
        )

        db.session.add(supplier)
        db.session.commit()

        return redirect("/suppliers")

    return render_template(
        "add_supplier.html"
    )

@app.route("/suppliers")
def suppliers():

    all_suppliers = Supplier.query.all()

    return render_template(
        "suppliers.html",
        suppliers=all_suppliers
    )

@app.route("/add-po", methods=["GET", "POST"])
def add_po():

    suppliers = Supplier.query.all()

    if request.method == "POST":

        print(request.form)

        po = PurchaseOrder(
            po_number=request.form["po_number"],
            supplier_id=request.form["supplier_id"],
            order_date=request.form["order_date"]
        )

        db.session.add(po)
        db.session.commit()

        return redirect("/purchase-orders")

    return render_template(
        "add_po.html",
        suppliers=suppliers
    )




@app.route("/purchase-orders")
def purchase_orders():

    all_pos = PurchaseOrder.query.all()

    return render_template(
        "purchase_orders.html",
        purchase_orders=all_pos
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

    session.clear()

    return redirect("/login")


@app.route("/delete-supplier/<int:id>")
def delete_supplier(id):

    supplier = Supplier.query.get_or_404(id)

    db.session.delete(supplier)

    db.session.commit()

    return redirect("/suppliers")


@app.route(
    "/edit-supplier/<int:id>",
    methods=["GET", "POST"]
)
def edit_supplier(id):

    supplier = Supplier.query.get_or_404(id)

    if request.method == "POST":

        supplier.supplier_code = request.form["supplier_code"]
        supplier.supplier_name = request.form["supplier_name"]
        supplier.contact_person = request.form["contact_person"]
        supplier.phone = request.form["phone"]
        supplier.email = request.form["email"]
        supplier.gst_number = request.form["gst_number"]
        supplier.address = request.form["address"]

        db.session.commit()

        return redirect("/suppliers")

    return render_template(
        "edit_supplier.html",
        supplier=supplier
    )


@app.route(
    "/po/<int:po_id>/add-item",
    methods=["GET", "POST"]
)
def add_po_item(po_id):

    items = Item.query.all()

    if request.method == "POST":

        quantity = float(
            request.form["quantity"]
        )

        rate = float(
            request.form["rate"]
        )

        line_total = quantity * rate

        po_item = PurchaseOrderItem(
            po_id=po_id,
            item_id=request.form["item_id"],
            quantity=quantity,
            rate=rate,
            line_total=line_total
        )

        db.session.add(po_item)

        po = PurchaseOrder.query.get(po_id)

        po.total_amount += line_total

        db.session.commit()

        return redirect(
            f"/purchase-order/{po_id}"
        )

    return render_template(
        "add_po_item.html",
        items=items
    )

@app.route("/purchase-order/<int:po_id>")
def purchase_order_details(po_id):

    po = PurchaseOrder.query.get_or_404(
        po_id
    )

    po_items = PurchaseOrderItem.query.filter_by(
        po_id=po_id
    ).all()

    return render_template(
        "po_details.html",
        po=po,
        po_items=po_items
    )


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