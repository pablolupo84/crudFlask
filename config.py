from decouple import config #para leer variables de entorno

class Config:
	SECRET_KEY = "srcoco3060"

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/project_web_facilito'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER =  'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'pablolupo84@gmail.com'
	#MAIL_PASSWORD = config('MAIL_PASSWORD') #variable de entorno
	MAIL_PASSWORD = 'srcoco3060'

class TestConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/project_web_facilito_test'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	TEST = True


config = {
	'development': DevelopmentConfig,
	'default':DevelopmentConfig,
	'test': TestConfig
}