from flask import (
    Blueprint,
    render_template,
    request,
    redirect
)

from models import (
    StockIssue,
    Inventory,
    Item,
    InventoryTransaction
)

from extensions import db

stock_issue_bp = Blueprint("stock_issue", __name__)


@stock_issue_bp.route(
    "/issue-stock",
    methods=["GET", "POST"]
)
def issue_stock():

    inventory = Inventory.query.all()

    if request.method == "POST":

        item_id = int(
            request.form["item_id"]
        )

        quantity = float(
            request.form["quantity"]
        )

        stock = Inventory.query.filter_by(
            item_id=item_id
        ).first()

        if stock.current_stock < quantity:
            return "Not enough stock!"

        # Reduce inventory
        stock.current_stock -= quantity

        # Create stock issue
        issue = StockIssue(
            item_id=item_id,
            quantity=quantity,
            issue_date=request.form["issue_date"],
            remarks=request.form["remarks"]
        )

        db.session.add(issue)

        # Generate issue.id before commit
        db.session.flush()

        # Record inventory transaction
        transaction = InventoryTransaction(
            item_id=item_id,
            transaction_type="ISSUE",
            quantity=quantity,
            reference_number=f"ISS-{issue.id}",
            remarks="Material Issued"
        )

        db.session.add(transaction)

        db.session.commit()

        return redirect("/inventory")

    return render_template(
        "issue_stock.html",
        inventory=inventory
    )


@stock_issue_bp.route("/stock-issues")
def stock_issues():

    all_issues = StockIssue.query.all()

    return render_template(
        "stock_issues.html",
        issues=all_issues
    )