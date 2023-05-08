from flask import Flask
from config import Config
from flask_sqlalchemy  import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import logging
from logging.handlers import SMTPHandler,RotatingFileHandler
import os



app = Flask(__name__)
load_dotenv()
#app configuration
app.config.from_object(Config)
#data base object
db = SQLAlchemy(app)
#migration engine
migrate = Migrate(app,db) 
#login manager 
login = LoginManager(app)
#set the login view that the login manage will redirect to when login is required
login.login_view = 'login'

#import routes for different views , and models for the database models
from . import routes,models,errors


if not app.debug:
    if app.config['EMAIL_SERVER']:
        auth = None
        if app.config['EMAIL_USERNAME'] or app.config['EMAIL_PASSWORD']:
            auth =( app.config['EMAIL_USERNAME'],app.config['EMAIL_PASSWORD'])

        secure = None
        if app.config['EMAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['EMAIL_SERVER'],app.config['EMAIL_PORT']),
            fromaddr='no-reply@' + app.config['EMAIL_SERVER'],
            toaddrs=app.config['ADMINS'],subject='Microblog Failure',
            credentials=auth,secure=secure)
        #this means only logs with a level of ERROR or higher will be sent
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log',maxBytes=10240,backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler) 
        app.logger.setLevel(logging.INFO)   
        app.logger.info('Microblog startup')