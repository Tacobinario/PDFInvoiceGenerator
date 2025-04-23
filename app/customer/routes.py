# app/customer/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Customer

customer = Blueprint('customer', __name__, url_prefix='/customer')

@customer.route('/new', methods=['GET', 'POST'])
def new():
	if request.method == 'POST':
		try:
			new_customer = Customer(
				name=request.form['name'],
				rfc=request.form['rfc'].upper(),
				email=request.form['email'],
				phone=request.form['phone'],
				address=request.form['address'],
				city=request.form['city'],
				postal_code=request.form['postal_code']
			)

			db.session.add(new_customer)
			db.session.commit()
			flash('Cliente registrado exitosamente', 'success')
			return redirect(url_for('customer.list'))

		except ValueError as e:
			flash(str(e), 'danger')
		except Exception as e:
			flash('Error al registrar el cliente', 'danger')
			db.session.rollback()

	return render_template('customer/new.html')

@customer.route('/list')
def list():
	customers = Customer.query.all()
	return render_template('customer/list.html', customers=customers)