from flask import (
    Blueprint,
    render_template,
    request
)

from models import (
    Inventory,
    Item
)

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/inventory")
def inventory():

    search = request.args.get("search", "")
    low_stock = request.args.get("low_stock", "")

    query = Inventory.query.join(Item)

    if search:

        query = query.filter(
            Item.material_name.ilike(f"%{search}%")
        )

    all_stock = query.all()

    if low_stock:

        all_stock = [
            stock for stock in all_stock
            if stock.item.min_stock
            and stock.current_stock < stock.item.min_stock
        ]

    return render_template(
        "inventory.html",
        inventory=all_stock,
        search=search,
        low_stock=low_stock
    )
