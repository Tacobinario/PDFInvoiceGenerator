# app/forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
	StringField, TextAreaField, FloatField, IntegerField,
	SelectField, DecimalField, SubmitField
)
from wtforms.validators import (
	DataRequired, Email, Length, Regexp, ValidationError,
	NumberRange
)

class CompanyForm(FlaskForm):
	name = StringField('Nombre de la Empresa', validators=[
		DataRequired(),
		Length(min=3, max=100)
	])
	rfc = StringField('RFC', validators=[
		DataRequired(),
		Regexp(r'^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$',
		       message='Formato de RFC inválido')
	])
	address = StringField('Dirección', validators=[
		DataRequired(),
		Length(max=200)
	])
	city = StringField('Ciudad', validators=[
		DataRequired(),
		Length(max=100)
	])
	postal_code = StringField('Código Postal', validators=[
		DataRequired(),
		Regexp(r'^\d{5}$', message='El código postal debe ser de 5 dígitos')
	])
	phone = StringField('Teléfono', validators=[
		DataRequired(),
		Regexp(r'^\+?[\d\s-]{10,20}$',
		       message='Formato de teléfono inválido')
	])
	email = StringField('Email', validators=[
		DataRequired(),
		Email(message='Dirección de email inválida')
	])
	logo = FileField('Logo de la Empresa', validators=[
		FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes!')
	])
	submit = SubmitField('Guardar Empresa')

class CustomerForm(FlaskForm):
	name = StringField('Nombre del Cliente', validators=[
		DataRequired(),
		Length(min=3, max=100)
	])
	rfc = StringField('RFC', validators=[
		DataRequired(),
		Regexp(r'^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$',
		       message='Formato de RFC inválido')
	])
	address = StringField('Dirección', validators=[
		DataRequired(),
		Length(max=200)
	])
	city = StringField('Ciudad', validators=[
		DataRequired(),
		Length(max=100)
	])
	postal_code = StringField('Código Postal', validators=[
		DataRequired(),
		Regexp(r'^\d{5}$', message='El código postal debe ser de 5 dígitos')
	])
	phone = StringField('Teléfono', validators=[
		DataRequired(),
		Regexp(r'^\+?[\d\s-]{10,20}$',
		       message='Formato de teléfono inválido')
	])
	email = StringField('Email', validators=[
		DataRequired(),
		Email(message='Dirección de email inválida')
	])
	submit = SubmitField('Guardar Cliente')

class InvoiceItemForm(FlaskForm):
	internal_id = StringField('ID Interno', validators=[
		DataRequired(),
		Length(max=50)
	])
	name = StringField('Nombre del Producto/Servicio', validators=[
		DataRequired(),
		Length(max=100)
	])
	description = TextAreaField('Descripción', validators=[
		Length(max=200)
	])
	quantity = IntegerField('Cantidad', validators=[
		DataRequired(),
		NumberRange(min=1)
	])
	unit_price = DecimalField('Precio Unitario', validators=[
		DataRequired(),
		NumberRange(min=0)
	])

class InvoiceForm(FlaskForm):
	customer_id = SelectField('Cliente', coerce=int, validators=[
		DataRequired()
	])
	currency = SelectField('Moneda', choices=[
		('MXN', 'Peso Mexicano (MXN)'),
		('USD', 'Dólar Estadounidense (USD)'),
		('BTC', 'Bitcoin (BTC)'),
		('DOGE', 'Dogecoin (DOGE)'),
		('ETH', 'Ethereum (ETH)')
	])
	payment_method = SelectField('Método de Pago', choices=[
		('transfer', 'Transferencia Bancaria'),
		('credit_card', 'Tarjeta de Crédito'),
		('btc', 'Bitcoin'),
		('doge', 'Dogecoin'),
		('eth', 'Ethereum'),
		('cash', 'Efectivo')
	])
	crypto_address = StringField('Dirección de Crypto (opcional)',
	                             validators=[Length(max=100)])
	submit = SubmitField('Generar Factura')

	def __init__(self, *args, **kwargs):
		super(InvoiceForm, self).__init__(*args, **kwargs)
		# Las opciones de customer_id se llenarán dinámicamente en la vista