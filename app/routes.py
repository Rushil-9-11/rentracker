from flask import Blueprint, request, jsonify, render_template
from .models import Tenant, RentPayment
from datetime import datetime
from . import db

# ✅ This defines the blueprint
main = Blueprint('main', __name__)

# ---------------------- API ROUTES ----------------------

@main.route('/tenants', methods=['POST'])
def add_tenant():
    data = request.get_json()

    new_tenant = Tenant(
        name=data['name'],
        apartment_number=data['apartment_number'],
        rent_amount=data['rent_amount'],
        due_day=data['due_day']
    )

    db.session.add(new_tenant)
    db.session.commit()

    return jsonify({"message": "Tenant added successfully"}), 201


@main.route('/tenants', methods=['GET'])
def get_tenants():
    tenants = Tenant.query.filter_by(is_active=True).all()
    
    output = []
    for tenant in tenants:
        tenant_data = {
            'id': tenant.id,
            'name': tenant.name,
            'apartment_number': tenant.apartment_number,
            'rent_amount': tenant.rent_amount,
            'due_day': tenant.due_day,
            'move_in_date': tenant.move_in_date.strftime('%Y-%m-%d')
        }
        output.append(tenant_data)
    
    return jsonify(output)


@main.route('/tenants/<int:tenant_id>/deactivate', methods=['PATCH'])
def deactivate_tenant(tenant_id):
    tenant = Tenant.query.get(tenant_id)
    
    if not tenant:
        return jsonify({"error": "Tenant not found"}), 404

    tenant.is_active = False
    db.session.commit()

    return jsonify({"message": "Tenant deactivated"}), 200


@main.route('/payments', methods=['POST'])
def record_payment():
    data = request.get_json()

    tenant_id = data['tenant_id']
    amount = data['amount']
    month = data['month']  # format: "2025-07"

    tenant = Tenant.query.get(tenant_id)

    if not tenant:
        return jsonify({"error": "Tenant not found"}), 404

    # Determine if late
    today = datetime.utcnow().day
    is_late = today > tenant.due_day

    payment = RentPayment(
        tenant_id=tenant_id,
        amount=amount,
        month=month,
        is_late=is_late
    )

    db.session.add(payment)
    db.session.commit()

    return jsonify({"message": "Rent payment recorded", "late": is_late}), 201


@main.route('/payments/income/<month>', methods=['GET'])
def get_monthly_income(month):
    payments = RentPayment.query.filter_by(month=month).all()
    total = sum(payment.amount for payment in payments)

    return jsonify({
        "month": month,
        "total_income": total,
        "payment_count": len(payments)
    })


@main.route('/payments/missed/<month>', methods=['GET'])
def get_missed_payments(month):
    all_tenants = Tenant.query.filter_by(is_active=True).all()
    paid_tenants = RentPayment.query.filter_by(month=month).with_entities(RentPayment.tenant_id).distinct()
    paid_ids = [pt.tenant_id for pt in paid_tenants]

    missed = [
        {
            "id": tenant.id,
            "name": tenant.name,
            "apartment_number": tenant.apartment_number
        }
        for tenant in all_tenants if tenant.id not in paid_ids
    ]

    return jsonify({
        "month": month,
        "missed_payments": missed
    })

# ---------------------- FRONTEND ROUTES ----------------------

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/tenants/view')
def view_tenants():
    tenants = Tenant.query.all()
    return render_template('tenants.html', tenants=tenants)


@main.route('/income/view')
def view_income():
    payments = RentPayment.query.all()
    return render_template('income.html', payments=payments)


@main.route('/missed/view')
def view_missed():
    month = request.args.get('month')
    missed = []

    if month:
        # Convert YYYY-MM to date range
        start_date = datetime.strptime(month, "%Y-%m")
        end_month = start_date.month % 12 + 1
        end_year = start_date.year + (1 if end_month == 1 else 0)
        end_date = datetime(end_year, end_month, 1)

        # Find active tenants
        active_tenants = Tenant.query.filter_by(is_active=True).all()

        for tenant in active_tenants:
            payment = RentPayment.query.filter(
                RentPayment.tenant_id == tenant.id,
                RentPayment.date >= start_date,
                RentPayment.date < end_date
            ).first()

            if not payment:
                missed.append(tenant)

    return render_template('missed.html', missed=missed, month=month)
