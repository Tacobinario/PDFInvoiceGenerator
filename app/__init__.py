# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Inicialización de extensiones
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	# Inicializar extensiones
	db.init_app(app)
	migrate.init_app(app, db)

	# Importar modelos para que Flask-Migrate los detecte
	from app import models

	# Asegurar que existe el directorio de uploads
	import os
	os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

	# Registrar blueprints
	from app.routes import main
	from app.api import api
	from app.company.routes import company
	from app.customer.routes import customer
	from app.invoice.routes import invoice

	app.register_blueprint(main)
	app.register_blueprint(api)
	app.register_blueprint(company)
	app.register_blueprint(customer)
	app.register_blueprint(invoice)

	return app