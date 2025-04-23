# add_sample_data.py
from app import create_app, db
from app.models import Company, Customer, Invoice, InvoiceItem
from datetime import datetime, timedelta

def add_sample_data():
	app = create_app()
	with app.app_context():
		# Limpiar datos existentes
		InvoiceItem.query.delete()
		Invoice.query.delete()
		Customer.query.delete()
		Company.query.delete()
		db.session.commit()

		# Crear empresas de ejemplo
		companies = [
			Company(
				name='TechSolutions SA de CV',
				rfc='TSO120524AB3',
				address='Av. Tecnológico 123',
				city='Ciudad de México',
				postal_code='01234',
				phone='55-1234-5678',
				email='contacto@techsolutions.com',
				logo_path='default_logo.png'
			),
			Company(
				name='Innovación Digital SA',
				rfc='IDA150630BC4',
				address='Calle Innovación 456',
				city='Guadalajara',
				postal_code='44100',
				phone='33-8765-4321',
				email='info@innovaciondigital.com',
				logo_path='default_logo.png'
			),
			Company(
				name='Servicios Web Plus',
				rfc='SWP180915CD5',
				address='Blvd. Internet 789',
				city='Monterrey',
				postal_code='64000',
				phone='81-9876-5432',
				email='contacto@webplus.com',
				logo_path='default_logo.png'
			)
		]

		for company in companies:
			db.session.add(company)

		# Crear clientes de ejemplo
		customers = [
			Customer(
				name='Comercial del Norte SA',
				rfc='CNO190528DE6',
				address='Av. Comercio 321',
				city='Tijuana',
				postal_code='22000',
				phone='664-111-2233',
				email='ventas@comercialnorte.com'
			),
			Customer(
				name='Distribuidora Centro',
				rfc='DCE200131EF7',
				address='Calle Centro 654',
				city='León',
				postal_code='37000',
				phone='477-444-5566',
				email='info@distcentro.com'
			),
			Customer(
				name='Servicios Industriales SA',
				rfc='SIN170725GH8',
				address='Zona Industrial 987',
				city='Querétaro',
				postal_code='76100',
				phone='442-777-8899',
				email='contacto@servindustrial.com'
			)
		]

		for customer in customers:
			db.session.add(customer)

		db.session.commit()

		# Crear facturas de ejemplo
		base_date = datetime.now()
		invoices = [
			Invoice(
				invoice_number='INV-20240301-001',
				date_created=base_date - timedelta(days=5),
				issuer=companies[0],
				customer=customers[0],
				subtotal=10000.00,
				tax_rate=0.16,
				tax_amount=1600.00,
				total=11600.00,
				currency='MXN',
				payment_method='transfer'
			),
			Invoice(
				invoice_number='INV-20240301-002',
				date_created=base_date - timedelta(days=3),
				issuer=companies[1],
				customer=customers[1],
				subtotal=25000.00,
				tax_rate=0.16,
				tax_amount=4000.00,
				total=29000.00,
				currency='MXN',
				payment_method='credit_card'
			),
			Invoice(
				invoice_number='INV-20240301-003',
				date_created=base_date - timedelta(days=1),
				issuer=companies[2],
				customer=customers[2],
				subtotal=5000.00,
				tax_rate=0.16,
				tax_amount=800.00,
				total=5800.00,
				currency='USD',
				payment_method='btc',
				crypto_address='1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
			)
		]

		for invoice in invoices:
			db.session.add(invoice)

			# Agregar items a cada factura
			items = [
				InvoiceItem(
					invoice=invoice,
					internal_id=f'PROD-{invoice.id}-1',
					name='Desarrollo Web',
					description='Desarrollo de sitio web responsivo',
					quantity=1,
					unit_price=5000.00,
					total_price=5000.00
				),
				InvoiceItem(
					invoice=invoice,
					internal_id=f'PROD-{invoice.id}-2',
					name='Hosting Anual',
					description='Servicio de hosting por un año',
					quantity=1,
					unit_price=2000.00,
					total_price=2000.00
				),
				InvoiceItem(
					invoice=invoice,
					internal_id=f'PROD-{invoice.id}-3',
					name='Mantenimiento',
					description='Servicio de mantenimiento mensual',
					quantity=12,
					unit_price=250.00,
					total_price=3000.00
				)
			]

			for item in items:
				db.session.add(item)

		db.session.commit()

if __name__ == '__main__':
	add_sample_data()
	print("Datos de ejemplo agregados exitosamente")