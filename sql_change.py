#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import db, models
userlist = models.User.query.all()
for user in userlist:
    user.posts_num = user.posts.count()
    user.follower_num = user.followers.count()
    user.followed_num = user.followed.count()
    db.session.add(user)
    if user.username in ('', None):
        db.session.delete(user)
db.session.commit()
for user in userlist:
    print(user.username)
    print(user.posts_num)
    print(user.follower_num)
    print(user.followed_num)