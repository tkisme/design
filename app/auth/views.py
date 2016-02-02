# coding=utf-8
# __author__ = 'tk'
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
# from ..email import send_email
from .forms import LoginForm, RegistrationForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        local_sms = db.session.query(Sms).filter(Sms.id == form.mobile.data).first()
        # print(form.code.data, local_sms.code)
        if int(form.code.data) == local_sms.code:
            print(form.code.data)
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(u'注册成功', 'success')
            return redirect(url_for('.login'))
        else:
            flash(u'验证码错误', 'warning')
            # user = User(email=form.email.data,
            #             username=form.username.data,
            #             password=form.password.data)
            # db.session.add(user)
            # db.session.commit()
            # token = user.generate_confirmation_token()
            # send_email(user.email, 'Confirm Your Account',
            #            'auth/email/confirm', user=user, token=token)
    # session['code'] = False
    # session.pop('code', None)
    return render_template('auth/register.html', form=form)
