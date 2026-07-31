from flask import (
    Blueprint,
    render_template,
    redirect,
    session
)

from sqlalchemy import extract, func

from extensions import db

from models import (
    Item,
    Supplier,
    PurchaseOrder,
    GRN,
    Inventory,
    StockIssue,
    InventoryTransaction
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def home():
    return "TPP Boilers ERP"


@dashboard_bp.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect("/login")

    # ==========================
    # Dashboard Statistics
    # ==========================

    total_items = Item.query.count()

    total_suppliers = Supplier.query.count()

    total_pos = PurchaseOrder.query.count()

    total_grns = GRN.query.count()

    total_stock_issues = StockIssue.query.count()

    # ==========================
    # Low Stock
    # ==========================

    low_stock_items = []

    all_inventory = Inventory.query.all()
    inventory_value = 0

    for stock in all_inventory:
        inventory_value += (
            stock.current_stock *
            stock.item.unit_price
    )
        
    for stock in all_inventory:

        if stock.item.min_stock:

            if stock.current_stock < stock.item.min_stock:

                low_stock_items.append(stock)

    # ==========================
    # Recent Activity
    # ==========================

    recent_pos = (
        PurchaseOrder.query
        .order_by(PurchaseOrder.id.desc())
        .limit(5)
        .all()
    )

    recent_grns = (
        GRN.query
        .order_by(GRN.id.desc())
        .limit(5)
        .all()
    )

    recent_issues = (
        StockIssue.query
        .order_by(StockIssue.id.desc())
        .limit(5)
        .all()
    )

    # ==========================
    # Purchase Orders by Month
    # ==========================

    po_chart = (
        db.session.query(
            extract("month", PurchaseOrder.order_date),
            db.func.count(PurchaseOrder.id)
        )
        .group_by(
            extract("month", PurchaseOrder.order_date)
        )
        .all()
    )

    month_names = [
        "",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]

    months = []

    counts = []

    for month, count in po_chart:
        print("Month =", month, "Count =", count)
        if month is None:
            continue
        months.append(month_names[int(month)])
        counts.append(count)
# ==========================
# Top Consumed Materials
# ==========================

    top_consumed = (
    db.session.query(
        Item.material_name,
        func.sum(InventoryTransaction.quantity).label("total_issued")
    )
    .join(
        InventoryTransaction,
        Item.id == InventoryTransaction.item_id
    )
    .filter(
        InventoryTransaction.transaction_type == "ISSUE"
    )
    .group_by(
        Item.id,
        Item.material_name
    )
    .order_by(
        func.sum(InventoryTransaction.quantity).desc()
    )
    .limit(5)
    .all()
)
    # ==========================
    # Render
    # ==========================

    return render_template(

        "dashboard.html",

        user=session["username"],

        total_items=total_items,

        total_suppliers=total_suppliers,

        total_pos=total_pos,

        total_grns=total_grns,

        total_stock_issues=total_stock_issues,

        low_stock_items=low_stock_items,

        recent_pos=recent_pos,

        recent_grns=recent_grns,

        recent_issues=recent_issues,

        months=months,

        counts=counts,

        inventory_value=inventory_value,

        top_consumed=top_consumed,

    )