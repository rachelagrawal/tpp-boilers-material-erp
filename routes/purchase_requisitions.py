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
    PurchaseRequisition
)

purchase_requisitions_bp = Blueprint(
    "purchase_requisitions",
    __name__
)


@purchase_requisitions_bp.route(
    "/purchase-requisitions",
    methods=["GET", "POST"]
)
def purchase_requisitions():

    if "username" not in session:
        return redirect("/login")

    items = Item.query.order_by(Item.material_name).all()

    if request.method == "POST":

        last_pr = PurchaseRequisition.query.order_by(
            PurchaseRequisition.id.desc()
        ).first()

        if last_pr:
            next_number = last_pr.id + 1
        else:
            next_number = 1

        pr = PurchaseRequisition(

            pr_number=f"PR-{next_number:04d}",

            item_id=request.form["item_id"],

            quantity=request.form["quantity"],

            department=request.form["department"],

            requested_by=request.form["requested_by"],

            purpose=request.form["purpose"],

            priority=request.form["priority"],

            request_date=request.form["request_date"]
        )

        db.session.add(pr)

        db.session.commit()

        return redirect("/purchase-requisitions")

    requisitions = PurchaseRequisition.query.order_by(
        PurchaseRequisition.id.desc()
    ).all()

    return render_template(
            "purchase_requisitions.html",
            items=items,
            requisitions=requisitions
        )

@purchase_requisitions_bp.route("/approve-pr/<int:id>")
def approve_pr(id):

    pr = PurchaseRequisition.query.get_or_404(id)

    pr.status = "Approved"

    db.session.commit()

    return redirect("/purchase-requisitions")

@purchase_requisitions_bp.route("/reject-pr/<int:id>")
def reject_pr(id):

    pr = PurchaseRequisition.query.get_or_404(id)

    pr.status = "Rejected"

    db.session.commit()

    return redirect("/purchase-requisitions")


    