# -*- coding: utf-8 -*-

class Config:    
    SECRET_KEY = 'a3071285de7d178a7ab64619baa691ed'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'passiton.cerner@gmail.com'#'sarora2k12@gmail.com'
    MAIL_PASSWORD = 'Welcome@2019'#'9897355445678'
    #os.environ.get('key')