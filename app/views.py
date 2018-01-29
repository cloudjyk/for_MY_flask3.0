#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import render_template, url_for, flash, redirect, session, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, avatars
from config import POSTS_PER_PAGE, USERS_PER_PAGE
from .forms import LoginForm, RegForm, PostForm, EditForm
from .models import User, Post
from datetime import datetime
from hashlib import md5

@app.before_request
def before_request():
    g.user = current_user


@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>',methods = ['GET', 'POST'])
@login_required
def index(page = 1):
    user = g.user
    form = PostForm()
    if form.validate_on_submit():
        body = form.body.data
        # p = Post(body = body, timestamp = datetime.utcnow(), author=g.user)
        p = Post(body = body, timestamp = datetime.utcnow(), user_id=g.user.get_id())
        db.session.add(p)
        db.session.commit()
        # form.body.data = ''
        # 防止重复提交
        return redirect(url_for('index'))
    posts = g.user.followed_posts()
    posts = posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('index.html',
        title = 'Home',
        user = user,
        form = form,
        posts = posts)

#从数据库加载用户
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods = ['GET', 'POST'])
# @oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if User.query.filter_by(username = form.username.data).first() == None:
            flash('Invalid user!')
            return redirect('/login')
        if User.query.filter_by(username = form.username.data).first().password != form.password.data:
            flash('Wrong password!')
            form.password.data = ''
            return redirect('/login')
        flash('Login successfully for user:"' + form.username.data + '", remember_me=' + str(form.remember_me.data))
        u = User.query.filter_by(username = form.username.data).first()
        u.last_seen = datetime.utcnow()
        # print(form.password.data)
        db.session.add(u)
        db.session.commit()
        login_user(u, form.remember_me.data)
        u = g.user.follow(g.user)
        if u != None:
            db.session.add(u)
            db.session.commit()
        return redirect('/index')
    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/register', methods = ['GET', 'POST'])
# @oid.loginhandler
def register():
    if g.user.is_authenticated:
        logout_user()
    form = RegForm()
    if form.validate_on_submit():
        if User.query.filter_by(username = form.username.data).first() != None:
            flash('This user already exists, please change your username!')
        elif not form.pw_check():
            # print(form.password.data,form.password2.data)
            flash('Passwords should be the same, please check!')
        elif not form.email_check():
            flash('Invalid email address!')
        else:
            u = User(username=form.username.data, password=md5(form.password.data.encode('utf-8')).hexdigest(), email=form.email.data)
            db.session.add(u)
            db.session.commit()
            flash('Register successfully for user:"' + form.username.data + '", remember_me=' + str(form.remember_me.data))
            return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/user/<username>', methods = ['GET', 'POST'])
@app.route('/user/<username>/<int:page>', methods = ['GET', 'POST'])
def user(username, page = 1):
    if User.query.filter_by(username = username).first() != None:
        user = User.query.filter_by(username = username).first()
        # posts = Post.query.filter_by(author = user).order_by(Post.timestamp.desc())
        posts = user.posts.order_by(Post.timestamp.desc())
        posts = posts.paginate(page, POSTS_PER_PAGE, False)
        return render_template('user.html',
            title = 'Home',
            user = user,
            posts = posts)
    flash('Sorry, this user does not exist!')
    return redirect(url_for('index'))

@app.route('/user/<username>/edit', methods = ['GET', 'POST'])
@login_required
def edit(username):
    if username != g.user.username:
        print(username,g.user.username)
        flash('You are not authorized to visit this page!')
        return redirect(url_for('index'))
    form = EditForm()
    if form.validate_on_submit():
        if form.username.data != g.user.username and User.query.filter_by(username = form.username.data).first() != None:
            flash('This username has been occupied!')
            return redirect(url_for('edit', username = g.user.username))
        else:
            if form.avatar.data:
                # print(form.avatar.data.stream)
                filename = avatars.save(form.avatar.data)
                # print(filename)
                file_url = avatars.url(filename)
                g.user.avatar = file_url
            g.user.username = form.username.data
            g.user.about_me = form.about_me.data
            u = g.user
            db.session.add(u)
            db.session.commit()
            logout_user()
            login_user(User.query.filter_by(username = form.username.data).first())
            flash('Your changes have been saved.')
            return redirect(url_for('user', username = form.username.data))
    else:
        form.username.data = g.user.username
        form.about_me.data = g.user.about_me
    return render_template('edit.html',
        title = 'Edit your info',
        user = g.user,
        form = form)

@app.route('/popular', methods = ['GET', 'POST'])
@app.route('/popular/<int:page>', methods = ['GET', 'POST'])
@login_required
def popular(page = 1):
    userlist = User.query.order_by(User.posts_num.desc())
    # userlist = User.query.order_by(User.followers.asc())
    print(userlist)
    print(g.user.followers.count())
    # for i in userlist:
    #     print(i)
    # userlist = sorted(userlist, key = lambda user: user.posts.count)
    userlist = userlist.paginate(page, USERS_PER_PAGE, False)
    print(userlist)
    return render_template('popular.html',
        title = 'popular',
        user = g.user,
        userlist = userlist)

@app.route('/follow/<username>', methods = ['GET', 'POST'])
@login_required
def follow(username):
    u = g.user.follow(User.query.filter_by(username = username).first())
    db.session.add(u)
    db.session.commit()
    flash('You have followed %s'%username)
    return redirect(url_for('user', username = username))

@app.route('/unfollow/<username>', methods = ['GET', 'POST'])
@login_required
def unfollow(username):
    u = g.user.unfollow(User.query.filter_by(username = username).first())
    db.session.add(u)
    db.session.commit()
    flash('You have unfollowed %s'%username)
    return redirect(url_for('user', username = username))

@app.route('/post_del/<post_id>')
@login_required
def post_del(post_id):
    p = Post.query.filter_by(id = post_id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('user', username = g.user.username))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# error customized

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500