# app/invoice/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.models import Invoice, InvoiceItem, Company, Customer
from datetime import datetime

invoice = Blueprint('invoice', __name__, url_prefix='/invoice')

@invoice.route('/new', methods=['GET', 'POST'])
def new():
	companies = Company.query.all()
	customers = Customer.query.all()

	if request.method == 'POST':
		try:
			# Crear nueva factura
			new_invoice = Invoice(
				issuer_id=request.form['issuer_id'],
				customer_id=request.form['customer_id'],
				invoice_number=f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
				subtotal=float(request.form['subtotal']),
				tax_rate=float(request.form.get('tax_rate', 0.16)),
				tax_amount=float(request.form['tax_amount']),
				total=float(request.form['total']),
				currency=request.form.get('currency', 'MXN'),
				payment_method=request.form['payment_method']
			)

			# Procesar items si se enviaron
			items_data = request.json.get('items', [])
			for item_data in items_data:
				item = InvoiceItem(
					invoice=new_invoice,
					internal_id=item_data['internal_id'],
					name=item_data['name'],
					description=item_data.get('description', ''),
					quantity=int(item_data['quantity']),
					unit_price=float(item_data['unit_price']),
					total_price=float(item_data['total_price'])
				)
				db.session.add(item)

			db.session.add(new_invoice)
			db.session.commit()

			flash('Factura creada exitosamente', 'success')
			return redirect(url_for('invoice.list'))

		except ValueError as e:
			flash(str(e), 'danger')
		except Exception as e:
			flash('Error al crear la factura', 'danger')
			db.session.rollback()

	return render_template('invoice/new.html', companies=companies, customers=customers)

@invoice.route('/list')
def list():
	invoices = Invoice.query.all()
	return render_template('invoice/list.html', invoices=invoices)