from flask import (
    Blueprint,
    render_template,
    request,
    redirect
)

from models import Supplier
from extensions import db

supplier_bp = Blueprint("suppliers", __name__)


@supplier_bp.route(
    "/add-supplier",
    methods=["GET", "POST"]
)
def add_supplier():

    if request.method == "POST":

        supplier = Supplier(
            supplier_code=request.form["supplier_code"],
            supplier_name=request.form["supplier_name"],
            contact_person=request.form["contact_person"],
            phone=request.form["phone"],
            email=request.form["email"],
            gst_number=request.form["gst_number"],
            address=request.form["address"]
        )

        db.session.add(supplier)
        db.session.commit()

        return redirect("/suppliers")

    return render_template(
        "add_supplier.html"
    )

@supplier_bp.route("/suppliers")
def suppliers():

    search = request.args.get("search", "")

    if search:

        all_suppliers = Supplier.query.filter(
            Supplier.supplier_name.ilike(f"%{search}%")
        ).all()

    else:

        all_suppliers = Supplier.query.all()

    return render_template(
        "suppliers.html",
        suppliers=all_suppliers,
        search=search
    )

@supplier_bp.route("/delete-supplier/<int:id>")
def delete_supplier(id):

    supplier = Supplier.query.get_or_404(id)

    db.session.delete(supplier)

    db.session.commit()

    return redirect("/suppliers")


@supplier_bp.route(
    "/edit-supplier/<int:id>",
    methods=["GET", "POST"]
)
def edit_supplier(id):

    supplier = Supplier.query.get_or_404(id)

    if request.method == "POST":

        supplier.supplier_code = request.form["supplier_code"]
        supplier.supplier_name = request.form["supplier_name"]
        supplier.contact_person = request.form["contact_person"]
        supplier.phone = request.form["phone"]
        supplier.email = request.form["email"]
        supplier.gst_number = request.form["gst_number"]
        supplier.address = request.form["address"]

        db.session.commit()

        return redirect("/suppliers")

    return render_template(
        "edit_supplier.html",
        supplier=supplier
    )