from app import app
from extensions import db
from models import *

from werkzeug.security import generate_password_hash
from datetime import date
import random

with app.app_context():

    db.drop_all()
    db.create_all()

    print("Creating demo database...")

    # ---------------- USERS ----------------

    admin = User(
        username="admin",
        password=generate_password_hash("admin123"),
        role="Admin"
    )

    demo = User(
        username="demo",
        password=generate_password_hash("demo123"),
        role="Store Manager"
    )

    db.session.add_all([admin, demo])

    # ---------------- SUPPLIERS ----------------

    supplier_names = [
        "Tata Steel",
        "Jindal Steel",
        "SKF Bearings",
        "L&T Industrial",
        "ABB India",
        "Siemens",
        "Ashoka Metals",
        "Prime Engineering"
    ]

    suppliers = []

    for i, name in enumerate(supplier_names, start=1):

        supplier = Supplier(
            supplier_code=f"SUP{i:03}",
            supplier_name=name,
            contact_person=f"Manager {i}",
            phone=f"98765432{i:02}",
            email=f"sales{i}@demo.com",
            gst_number=f"24ABCDE{i:05}F1Z5",
            address="Vadodara, Gujarat"
        )

        suppliers.append(supplier)

    db.session.add_all(suppliers)

    # ---------------- ITEMS ----------------

    materials = [
        ("Steel Plate 8mm","Steel"),
        ("Steel Rod 20mm","Steel"),
        ("Boiler Tube","Tube"),
        ("Bearing 6205","Bearing"),
        ("Bearing 6206","Bearing"),
        ("Industrial Paint","Paint"),
        ("Welding Electrode","Consumable"),
        ("MS Channel","Steel"),
        ("MS Angle","Steel"),
        ("Copper Wire","Electrical"),
        ("Control Panel","Electrical"),
        ("Pressure Gauge","Instrument"),
        ("Valve 2 Inch","Valve"),
        ("Valve 4 Inch","Valve"),
        ("Nut M12","Hardware"),
        ("Bolt M12","Hardware"),
        ("Boiler Shell","Assembly"),
        ("Pump Motor","Mechanical"),
        ("Gasket Sheet","Consumable"),
        ("GI Pipe","Pipe"),
        ("Flange","Pipe"),
        ("Safety Valve","Valve"),
        ("Thermocouple","Instrument"),
        ("Insulation Wool","Insulation"),
        ("Industrial Lubricant","Oil")
    ]

    items = []

    for i, (name, cat) in enumerate(materials, start=1):

        item = Item(
            item_code=f"MAT{i:03}",
            material_name=name,
            category=cat,
            specification="Standard",
            uom="Nos",
            min_stock=20,
            max_stock=300,
            unit_price=random.randint(100,5000)
        )

        items.append(item)

    db.session.add_all(items)

    db.session.commit()

    print("Users, Suppliers and Items created.")
        # ---------------- INVENTORY ----------------

    inventory_records = []

    for item in items:

        stock = random.randint(30, 250)

        inventory_records.append(

            Inventory(
                item_id=item.id,
                current_stock=stock
            )

        )

    db.session.add_all(inventory_records)

    # ---------------- PURCHASE REQUISITIONS ----------------

    departments = [
        "Production",
        "Maintenance",
        "Quality",
        "Stores",
        "Projects"
    ]

    requisitions = []

    for i in range(12):

        pr = PurchaseRequisition(

            pr_number=f"PR{i+1:03}",

            item_id=random.choice(items).id,

            quantity=random.randint(10,80),

            department=random.choice(departments),

            requested_by=f"Employee {i+1}",

            purpose="Production Requirement",

            priority=random.choice(
                ["Low","Medium","High"]
            ),

            status="Approved"

        )

        requisitions.append(pr)

    db.session.add_all(requisitions)

    db.session.commit()

    # ---------------- PURCHASE ORDERS ----------------

    purchase_orders = []

    for i, pr in enumerate(requisitions):

        po = PurchaseOrder(

            po_number=f"PO{i+1:03}",

            supplier_id=random.choice(
                suppliers
            ).id,

            order_date="2026-07-20",

            status=random.choice([
                "Approved",
                "Pending",
                "Received"
            ]),

            total_amount=0,

            pr_id=pr.id

        )

        purchase_orders.append(po)

    db.session.add_all(purchase_orders)

    db.session.commit()

    # ---------------- PO ITEMS ----------------

    for po in purchase_orders:

        item = random.choice(items)

        qty = random.randint(5,60)

        rate = item.unit_price

        db.session.add(

            PurchaseOrderItem(

                po_id=po.id,

                item_id=item.id,

                quantity=qty,

                rate=rate,

                line_total=qty * rate

            )

        )

        po.total_amount = qty * rate

    db.session.commit()

    print("Inventory, PRs and Purchase Orders created.")
        # ---------------- GRNs ----------------

    for i, po in enumerate(purchase_orders):

        grn = GRN(
            grn_number=f"GRN{i+1:03}",
            po_id=po.id,
            received_date="2026-07-25",
            status="Received"
        )

        db.session.add(grn)

    db.session.commit()

    # ---------------- STOCK ISSUES ----------------

    for i in range(20):

        item = random.choice(items)

        db.session.add(

            StockIssue(
                item_id=item.id,
                quantity=random.randint(1,15),
                issue_date="2026-07-28",
                remarks="Production Issue"
            )

        )

    db.session.commit()

    # ---------------- MATERIAL RETURNS ----------------

    for i in range(10):

        item = random.choice(items)

        db.session.add(

            MaterialReturn(
                item_id=item.id,
                quantity=random.randint(1,5),
                return_date=date.today(),
                reason="Unused Material"
            )

        )

    db.session.commit()

    # ---------------- INVENTORY TRANSACTIONS ----------------

    for i in range(40):

        item = random.choice(items)

        db.session.add(

            InventoryTransaction(
                item_id=item.id,
                transaction_type=random.choice([
                    "GRN",
                    "Issue",
                    "Return"
                ]),
                quantity=random.randint(1,20),
                reference_number=f"REF{i+1:03}",
                remarks="Demo Transaction"
            )

        )

    db.session.commit()

    # ---------------- AUDIT LOGS ----------------

    users = User.query.all()

    actions = [
        "Created Purchase Order",
        "Issued Stock",
        "Added Supplier",
        "Updated Inventory",
        "Received Goods",
        "Created Item",
        "Approved Purchase Order",
        "Returned Material"
    ]

    for i in range(30):

        db.session.add(

            AuditLog(
                user_id=random.choice(users).id,
                action=random.choice(actions)
            )

        )

    db.session.commit()

    print("=" * 50)
    print("DEMO ERP CREATED SUCCESSFULLY")
    print("=" * 50)
    print("Login Credentials")
    print()
    print("Admin")
    print("Username : admin")
    print("Password : admin123")
    print()
    print("Demo User")
    print("Username : demo")
    print("Password : demo123")
    print("=" * 50)