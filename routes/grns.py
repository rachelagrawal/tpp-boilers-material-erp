from flask import (
    Blueprint,
    render_template,
    request,
    redirect
)

from models import (
    GRN,
    PurchaseOrder,
    PurchaseOrderItem,
    Inventory
)

from extensions import db
from models import InventoryTransaction
grn_bp = Blueprint("grns", __name__)


@grn_bp.route(
    "/add-grn",
    methods=["GET", "POST"]
)
def add_grn():

    purchase_orders = PurchaseOrder.query.all()

    if request.method == "POST":

        grn = GRN(
            grn_number=request.form["grn_number"],
            po_id=request.form["po_id"],
            received_date=request.form["received_date"]
        )

        db.session.add(grn)
        po = PurchaseOrder.query.get(int(request.form["po_id"]))
        po.status = "Completed"
        
        po_items = PurchaseOrderItem.query.filter_by(
            po_id=request.form["po_id"]
        ).all()
        
        for po_item in po_items:
            stock = Inventory.query.filter_by(
                item_id=po_item.item_id
            ).first()
            if stock:
                stock.current_stock += po_item.quantity

            else:
                stock = Inventory(
                    item_id=po_item.item_id,
                    current_stock=po_item.quantity
                )

                db.session.add(stock)
                transaction = InventoryTransaction(
                    item_id=po_item.item_id,
                    transaction_type="GRN",
                    quantity=po_item.quantity,
                    reference_number=grn.grn_number,
                    remarks="Goods Received"
                )

                db.session.add(transaction)
        db.session.commit()

        return redirect("/grns")

    return render_template(
        "add_grn.html",
        purchase_orders=purchase_orders
    )

@grn_bp.route("/grns")
def grns():

    all_grns = GRN.query.all()

    return render_template(
        "grns.html",
        grns=all_grns
    )


