#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField

from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

from wtforms.validators import DataRequired, Length
import re

photos = UploadSet('photos', IMAGES)

class LoginForm(FlaskForm):
    """docstring for LoginForm"""
    # def __init__(self, arg):
    #     super(LoginForm, self).__init__()
    #     self.arg = arg
    username = StringField('username',validators=[DataRequired()])
    password = StringField('password',validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default = True)

class RegForm(FlaskForm):
    """docstring for LoginForm"""
    # def __init__(self, arg):
    #     super(LoginForm, self).__init__()
    #     self.arg = arg
    username = StringField('username',validators=[DataRequired()])
    password = StringField('password',validators=[DataRequired()])
    password2 = StringField('password2',validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default = True)
    def pw_check(self):
        if self.password.data == self.password2.data:
            return True
    def email_check(self):
        if re.match(r'^[0-9a-zA-Z][0-9a-zA-Z\-\_\s]*@[a-zA-Z0-9]+\.com(\.cn)?$', self.email.data):
            return True

class PostForm(FlaskForm):
    body = TextAreaField('body',validators=[DataRequired()])

class EditForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    about_me = StringField('about_me',validators=[Length(min=1, max=140)])
    avatar = FileField('avatar')
    # avatar = FileField('avatar',validators=[FileAllowed(photos, u'只能上传图片！'),FileRequired(u'文件未选择!')])

