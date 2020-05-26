class Config:
	SECRET_KEY = "srcoco3060"

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/project_web_facilito'

config = {
	'development': DevelopmentConfig,
	'default':DevelopmentConfig
}