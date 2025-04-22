# app/models.py
from datetime import datetime
from app import db
from sqlalchemy.orm import validates
import re

class Company(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	rfc = db.Column(db.String(13), nullable=False, unique=True)
	address = db.Column(db.String(200), nullable=False)
	city = db.Column(db.String(100), nullable=False)
	postal_code = db.Column(db.String(5), nullable=False)
	phone = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(120), nullable=False)
	logo_path = db.Column(db.String(255))

	# Relaciones
	invoices_issued = db.relationship('Invoice', backref='issuer', lazy='dynamic')

	@validates('rfc')
	def validate_rfc(self, key, rfc):
		# Validación básica de RFC (ajustar según necesidades específicas)
		if not re.match(r'^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$', rfc):
			raise ValueError('Formato de RFC inválido')
		return rfc

	@validates('postal_code')
	def validate_postal_code(self, key, postal_code):
		if not re.match(r'^\d{5}$', postal_code):
			raise ValueError('Código postal debe ser de 5 dígitos')
		return postal_code

class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	rfc = db.Column(db.String(13), nullable=False)
	address = db.Column(db.String(200), nullable=False)
	city = db.Column(db.String(100), nullable=False)
	postal_code = db.Column(db.String(5), nullable=False)
	phone = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(120), nullable=False)

	# Relaciones
	invoices = db.relationship('Invoice', backref='customer', lazy='dynamic')

class Invoice(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	invoice_number = db.Column(db.String(20), unique=True, nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	# Relaciones con Company y Customer
	issuer_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

	# Campos financieros
	subtotal = db.Column(db.Float, nullable=False)
	tax_rate = db.Column(db.Float, default=0.16)  # 16% IVA
	tax_amount = db.Column(db.Float, nullable=False)
	total = db.Column(db.Float, nullable=False)

	# Moneda y conversiones
	currency = db.Column(db.String(3), nullable=False, default='MXN')
	usd_rate = db.Column(db.Float)  # Tipo de cambio USD al momento de crear

	# Método de pago
	payment_method = db.Column(db.String(20), nullable=False)
	crypto_address = db.Column(db.String(100))  # Para pagos en crypto

	# Relaciones
	items = db.relationship('InvoiceItem', backref='invoice', lazy='dynamic')

	@validates('payment_method')
	def validate_payment_method(self, key, method):
		valid_methods = ['transfer', 'credit_card', 'btc', 'doge', 'eth', 'cash']
		if method not in valid_methods:
			raise ValueError(f'Método de pago inválido. Debe ser uno de: {", ".join(valid_methods)}')
		return method

	def generate_invoice_number(self):
		"""Genera número de factura basado en fecha/hora y secuencia"""
		timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
		sequence = f"{self.id:04d}"  # Rellena con ceros a la izquierda
		return f"{timestamp}-{sequence}"

class InvoiceItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)

	# Detalles del item
	internal_id = db.Column(db.String(50), nullable=False)
	name = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(200))  # Máximo 20 palabras
	quantity = db.Column(db.Integer, nullable=False)
	unit_price = db.Column(db.Float, nullable=False)
	total_price = db.Column(db.Float, nullable=False)

	@validates('description')
	def validate_description(self, key, description):
		if description and len(description.split()) > 20:
			raise ValueError('La descripción no puede exceder 20 palabras')
		return description

	def calculate_total(self):
		"""Calcula el precio total del ítem"""
		return self.quantity * self.unit_price