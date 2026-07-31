from flask import (
    Blueprint,
    render_template,
    request,
    redirect
)

from models import Item
from extensions import db
from utils.auth import require_role
from audit import log_action
item_bp = Blueprint("items", __name__)

@item_bp.route("/items")
def items():
    require_role(
        "Admin",
        "Purchase Manager",
        "Store Manager",
        "Viewer"
    )
    search = request.args.get("search", "")

    if search:

        all_items = Item.query.filter(
            Item.material_name.ilike(f"%{search}%")
        ).all()

    else:

        all_items = Item.query.all()

    return render_template(
        "items.html",
        items=all_items,
        search=search
    )

@item_bp.route("/add-item", methods=["GET", "POST"])
def add_item():

    require_role(
        "Admin"
    )

    if request.method == "POST":

        item = Item(
            item_code=request.form["item_code"],
            material_name=request.form["material_name"],
            category=request.form["category"],
            specification=request.form["specification"],
            uom=request.form["uom"],
            min_stock=request.form["min_stock"] or 0,
            max_stock=request.form["max_stock"] or 0,
            unit_price=request.form["unit_price"] or 0
        )

        db.session.add(item)
        db.session.commit()

        log_action(f"Added Item: {item.material_name}")

        return redirect("/items")

    return render_template("add_item.html")

@item_bp.route("/edit-item/<int:id>", methods=["GET", "POST"])
def edit_item(id):

    item = Item.query.get_or_404(id)

    if request.method == "POST":

        item.item_code = request.form["item_code"]

        item.material_name = request.form["material_name"]

        item.category = request.form["category"]

        item.specification = request.form["specification"]

        item.uom = request.form["uom"]

        item.min_stock = request.form["min_stock"]

        item.max_stock = request.form["max_stock"]

        item.unit_price = request.form["unit_price"]

        db.session.commit()

        return redirect("/items")

    return render_template(
        "edit_item.html",
        item=item
    )
