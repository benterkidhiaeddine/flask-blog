import os
#name of the directory where the project resides
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "random-password-that-you-will-never-guess"
    #define where the database is going to reside it gets from the environment variable if it exist else it will give a default value
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{os.path.join(basedir,'app.db')}"
    #this is to get a performance boost and not get notifications each time there is a change in the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    TEMPLATES_AUTO_RELOAD = True

    #email configuration 

    EMAIL_SERVER = os.environ.get("EMAIL_SERVER")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT") or 25)
    #to make sure we are using tls a encrypted connection
    EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS") is not None 
    EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    #put inside this list the emails of the admins you want to send the error logs to 
    ADMINS = ["thekizzer.swag@gmail.com"]