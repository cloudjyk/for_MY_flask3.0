#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# config initialed
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
avatars = UploadSet('AVATARS', IMAGES)
configure_uploads(app, avatars)
patch_request_class(app)

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
#设置登录视图，很关键
lm.login_view = 'login'


# time module
from .momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs

# debug
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
if not app.debug:
    import logging
    # email
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    # file
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')

from app import views, forms, models