# config.py
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
	# Configuración básica
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-very-secret'

	# Configuración de la base de datos
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	                          'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Configuración para subida de archivos
	UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads/logos')
	MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
	ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

	# APIs (añadiremos las keys después)
	EXCHANGE_RATE_API_KEY = os.environ.get('EXCHANGE_RATE_API_KEY')
	COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'