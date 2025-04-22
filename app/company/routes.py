# app/company/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Company
import os
from werkzeug.utils import secure_filename
from config import Config

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/new', methods=['GET', 'POST'])
def new():
	if request.method == 'POST':
		try:
			# Crear nueva empresa
			new_company = Company(
				name=request.form['name'],
				rfc=request.form['rfc'].upper(),
				email=request.form['email'],
				phone=request.form['phone'],
				address=request.form['address'],
				city=request.form['city'],
				postal_code=request.form['postal_code']
			)

			# Manejar el logo si se subió uno
			if 'logo' in request.files:
				logo = request.files['logo']
				if logo and logo.filename:
					filename = secure_filename(f"{new_company.rfc}_{logo.filename}")
					logo_path = os.path.join(Config.UPLOAD_FOLDER, filename)
					logo.save(logo_path)
					new_company.logo_path = filename

			db.session.add(new_company)
			db.session.commit()
			flash('Empresa registrada exitosamente', 'success')
			return redirect(url_for('company.list'))

		except ValueError as e:
			flash(str(e), 'danger')
		except Exception as e:
			flash('Error al registrar la empresa', 'danger')
			db.session.rollback()

	return render_template('company/new.html')

@company.route('/list')
def list():
	companies = Company.query.all()
	return render_template('company/list.html', companies=companies)