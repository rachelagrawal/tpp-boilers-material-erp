from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

from extensions import db

from models import (
    Item,
    Inventory,
    MaterialReturn,
    InventoryTransaction
)

material_return_bp = Blueprint(
    "material_return",
    __name__
)


@material_return_bp.route("/material-return", methods=["GET", "POST"])
def material_return():

    if "username" not in session:
        return redirect("/login")

    items = Item.query.order_by(Item.material_name).all()

    if request.method == "POST":

        item_id = int(request.form["item_id"])
        quantity = float(request.form["quantity"])

        stock = Inventory.query.filter_by(
            item_id=item_id
        ).first()

        if stock:
            stock.current_stock += quantity
        else:
            stock = Inventory(
                item_id=item_id,
                current_stock=quantity
            )
            db.session.add(stock)

        material_return = MaterialReturn(
            item_id=item_id,
            quantity=quantity,
            return_date=request.form["return_date"],
            reason=request.form["reason"]
        )

        db.session.add(material_return)

        db.session.flush()

        transaction = InventoryTransaction(
            item_id=item_id,
            transaction_type="RETURN",
            quantity=quantity,
            reference_number=f"RET-{material_return.id}",
            remarks="Material Returned"
        )

        db.session.add(transaction)

        db.session.commit()

        return redirect("/material-return")

    returns = (
        MaterialReturn.query
        .order_by(MaterialReturn.id.desc())
        .all()
    )

    return render_template(
        "material_return.html",
        items=items,
        returns=returns
    )