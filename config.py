# ID 配置
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

USER_LIST = [
    { 'username': 'cloudjyk1', 'password': 'cf2787ebc91a61313ac76ada9df35e50', 'email': 'cloudjyk@yahoo.com'},
    { 'username': 'cloudjyk02', 'password': 'cf2787ebc91a61313ac76ada9df35e50', 'email': 'cloudjyk02@yahoo.com'},
    { 'username': 'cloudjyk01', 'password': 'cf2787ebc91a61313ac76ada9df35e50', 'email': 'cloudjyk@yahoo.com'},
    { 'username': 'cloudjyk022', 'password': 'cf2787ebc91a61313ac76ada9df35e50', 'email': 'cloudjyk02@yahoo.com'},
    { 'username': 'cloudjyk0222', 'password': 'cf2787ebc91a61313ac76ada9df35e50', 'email': 'cloudjyk02@yahoo.com'}]


import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# pagination
POSTS_PER_PAGE = 3

# email inform
# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['you@example.com']

# avatars
from flask_uploads import IMAGES
# mac
# UPLOADED_AVATARS_DEST = basedir+'/app/sources/avatars'
# windows
UPLOADED_AVATARS_DEST = basedir+'\\app\\sources\\avatars'
UPLOADED_AVATARS_ALLOW = IMAGES