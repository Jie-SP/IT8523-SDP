import os
 
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://freedb_suser:5F5GKq%40mFvm4p2p@sql.freedb.tech:3306/freedb_mydatabase'
    # Example MySQL connection string
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://user:password@http://localhost:3306/mydatabase'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:example@dbMySQL:3306/mydatabase2'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://kimhoe.gcit:P06coqOWytAT@ep-little-hall-a1ykg9bf.ap-southeast-1.aws.neon.tech/usmdb'
 
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
 
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
