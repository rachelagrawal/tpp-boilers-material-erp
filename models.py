from extensions import db
from datetime import date
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

    role = db.Column(
    db.String(30),
    nullable=False,
    default="Viewer"
    )

    role = db.Column(
    db.String(30),
    nullable=False,
    default="Store Manager"
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

    unit_price = db.Column(
    db.Float,
    default=0
    )

    unit_price = db.Column(
    db.Float,
    default=0
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

    pr_id = db.Column(
    db.Integer,
    db.ForeignKey("purchase_requisitions.id")
    )
    purchase_requisition = db.relationship(
    "PurchaseRequisition"
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

class GRN(db.Model):
    __tablename__ = "grns"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    grn_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    po_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "purchase_orders.id"
        )
    )

    received_date = db.Column(
        db.String(20)
    )

    status = db.Column(
        db.String(50),
        default="Received"
    )

    purchase_order = db.relationship(
        "PurchaseOrder"
    )

class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.id"),
        unique=True
    )

    current_stock = db.Column(
        db.Float,
        default=0
    )

    item = db.relationship(
        "Item"
    )

class StockIssue(db.Model):
    __tablename__ = "stock_issues"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.id")
    )

    quantity = db.Column(
        db.Float
    )

    issue_date = db.Column(
        db.String(20)
    )

    remarks = db.Column(
        db.String(255)
    )

    item = db.relationship(
        "Item"
    )

from datetime import datetime

from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    action = db.Column(
        db.String(255),
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="audit_logs"
    )

class InventoryTransaction(db.Model):
    __tablename__ = "inventory_transactions"

    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.id"),
        nullable=False
    )

    transaction_type = db.Column(
        db.String(30),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    reference_number = db.Column(
        db.String(30)
    )

    remarks = db.Column(
        db.String(200)
    )

    transaction_date = db.Column(
        db.Date,
        default=date.today
    )

    item = db.relationship("Item")

class MaterialReturn(db.Model):
    __tablename__ = "material_returns"

    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Float,
        nullable=False
    )

    return_date = db.Column(
        db.Date,
        nullable=False
    )

    reason = db.Column(
        db.String(200)
    )

    item = db.relationship("Item")   

class InventoryAdjustment(db.Model):
    __tablename__ = "inventory_adjustments"

    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.id"),
        nullable=False
    )

    adjustment_quantity = db.Column(
        db.Float,
        nullable=False
    )

    adjustment_date = db.Column(
        db.Date,
        nullable=False
    )

    reason = db.Column(
        db.String(200)
    )

    item = db.relationship("Item")   

from datetime import date

class PurchaseRequisition(db.Model):
    __tablename__ = "purchase_requisitions"

    id = db.Column(db.Integer, primary_key=True)

    pr_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Float,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    requested_by = db.Column(
        db.String(100),
        nullable=False
    )

    purpose = db.Column(
        db.String(250)
    )

    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    request_date = db.Column(
        db.Date,
        default=date.today
    )

    item = db.relationship("Item")