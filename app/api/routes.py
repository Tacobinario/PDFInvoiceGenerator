from flask import jsonify, request
from app.api import api
from app.models import Company, Customer
from app import db
import re

@api.route('/validate_rfc', methods=['POST'])
def validate_rfc():
	data = request.get_json()
	if not data or 'rfc' not in data:
		return jsonify({'valid': False, 'message': 'No se proporcionó RFC'}), 400

	rfc = data['rfc'].upper()

	# Validación de formato
	if not re.match(r'^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$', rfc):
		return jsonify({
			'valid': False,
			'message': 'Formato de RFC inválido'
		}), 400

	# Verificar si ya existe
	existing_company = Company.query.filter_by(rfc=rfc).first()
	existing_customer = Customer.query.filter_by(rfc=rfc).first()

	if existing_company or existing_customer:
		return jsonify({
			'valid': False,
			'message': 'Este RFC ya está registrado'
		}), 400

	# Validaciones adicionales específicas de México
	tipo_persona = 'moral' if len(rfc) == 12 else 'física'

	# Validar fecha en el RFC
	fecha = rfc[4:10]  # AAMMDD
	try:
		año = int(fecha[:2])
		mes = int(fecha[2:4])
		dia = int(fecha[4:])

		if mes < 1 or mes > 12:
			return jsonify({
				'valid': False,
				'message': 'Mes inválido en el RFC'
			}), 400

		if dia < 1 or dia > 31:
			return jsonify({
				'valid': False,
				'message': 'Día inválido en el RFC'
			}), 400

	except ValueError:
		return jsonify({
			'valid': False,
			'message': 'Fecha inválida en el RFC'
		}), 400

	return jsonify({
		'valid': True,
		'message': f'RFC válido para persona {tipo_persona}',
		'type': tipo_persona
	})