import os
basedir = os.path.abspath(os.path.dirname(__file__))

class config():
	DEBUG = True
	SQLITE_DB_DIR = None
	SQLALCHEMY_DATABASE_URI = None
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECURITIY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"


class DevelopmentEnviroment(config):
	print(basedir)
	# SQLITE_DB_DIR = os.path.join(basedir[:-6], 'database', 'blog_lite_test2.sqlite3')
	# SQLITE_DB_DIR = os.path.join(basedir[:-6], 'database', 'database.sqlite3')
	SQLITE_DB_DIR = os.path.join(basedir[:-6], 'database', 'app_dev_2_test_db.sqlite3')
	
	print('final dir is:', SQLITE_DB_DIR)
	SQLALCHEMY_DATABASE_URI = "sqlite:///" +SQLITE_DB_DIR
	print(SQLALCHEMY_DATABASE_URI)

