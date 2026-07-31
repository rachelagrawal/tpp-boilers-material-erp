from flask import (
    Blueprint,
    render_template,
    request,
    redirect
)

from models import (
    PurchaseOrder,
    PurchaseOrderItem,
    Supplier,
    Item
)

from extensions import db

po_bp = Blueprint("purchase_orders", __name__)

@po_bp.route("/add-po", methods=["GET", "POST"])
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




@po_bp.route("/purchase-orders")
def purchase_orders():

    search = request.args.get("search", "")
    status = request.args.get("status", "")

    query = PurchaseOrder.query.join(Supplier)

    if search:

        query = query.filter(
            db.or_(
                PurchaseOrder.po_number.ilike(f"%{search}%"),
                Supplier.supplier_name.ilike(f"%{search}%")
            )
        )

    if status:

        query = query.filter(
            PurchaseOrder.status == status
        )

    all_pos = query.all()

    return render_template(
        "purchase_orders.html",
        purchase_orders=all_pos,
        search=search,
        status=status
    )







@po_bp.route(
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


@po_bp.route("/purchase-order/<int:po_id>")
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