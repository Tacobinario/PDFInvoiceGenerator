# app/company/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Company
from app.forms import CompanyForm  # Importar el formulario
import os
from werkzeug.utils import secure_filename
from config import Config

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/new', methods=['GET', 'POST'])
def new():
	form = CompanyForm()  # Crear instancia del formulario

	if form.validate_on_submit():
		try:
			# Crear nueva empresa usando los datos del formulario
			new_company = Company(
				name=form.name.data,
				rfc=form.rfc.data.upper(),
				email=form.email.data,
				phone=form.phone.data,
				address=form.address.data,
				city=form.city.data,
				postal_code=form.postal_code.data
			)

			# Manejar el logo si se subió uno
			if form.logo.data:
				logo = form.logo.data
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

	return render_template('company/new.html', form=form)  # Pasar el formulario a la plantilla

@company.route('/list')
def list():
	companies = Company.query.all()
	return render_template('company/list.html', companies=companies)