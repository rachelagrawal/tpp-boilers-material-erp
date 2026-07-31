from flask import Blueprint, render_template

from models import InventoryTransaction

inventory_history_bp = Blueprint(
    "inventory_history",
    __name__
)


@inventory_history_bp.route("/inventory-history")
def inventory_history():

    transactions = InventoryTransaction.query.order_by(
        InventoryTransaction.transaction_date.desc(),
        InventoryTransaction.id.desc()
    ).all()

    return render_template(
        "inventory_history.html",
        transactions=transactions
    )