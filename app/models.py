#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import app, db
from hashlib import md5
import sys

# for search
# if sys.version_info >= (3, 0):
#     enable_search = False
# else:
#     enable_search = True
#     import flask.ext.whooshalchemy as whooshalchemy
# for search
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(64), index = True)
    avatar = db.Column(db.String(140), index = True)
    email = db.Column(db.String(120), index = True, unique = True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    posts_num = db.Column(db.Integer)
    follower_num = db.Column(db.Integer)
    followed_num = db.Column(db.Integer)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User',
        secondary = followers,
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id),
        backref = db.backref('followers', lazy = 'dynamic'),
        lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return  False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.username

    # def avatar(self,size):
    #     # return 'http://www.gravatar.com/avatar/' + '205e460b479e2e5b48aec07710c08d50' + '?d=mm&s=' + str(size)
    #     return 'http://www.gravatar.com/avatar/' + md5(self.email.encode('utf-8')).hexdigest() + '?d=mm&s=' + str(size)
    @staticmethod
    def make_unique_nickname(username):
        if User.query.filter_by(username = username).first() == None:
            return username
        version = 2
        while True:
            new_username = username + str(version)
            if User.query.filter_by(username = new_username).first() == None:
                break
            version += 1
        return new_username

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # def follower_count(self):
    #     return self.followers.filter(followers.c.follower_id == self.id).count()

    def followed_posts(self):
        return Post.query.join(followers,
         (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

class Post(db.Model):
    # for search
    __searchable__ = ['body']
    # for search
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
# for search
# if enable_search:
#     whooshalchemy.whoosh_index(app, Post)
# for search