# coding=utf-8
# __author__ = 'tk'
from sqlalchemy import exc
from flask import render_template, redirect, request, url_for, flash, jsonify
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import auth, random_gen, sms
from .. import db
from ..models import User, Sms
# from ..email import send_email
from .forms import LoginForm, RegistrationForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        print(request.endpoint)
        # current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static' \
                and request.endpoint != 'bootstrap.static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # flash(u'注册成功', 'success')
    # return redirect(url_for('main.index'))
    # flash(u'注册成功', 'success')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            # print('login')
            login_user(user, form.remember_me.data)
            flash(u'登录成功', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或密码错误', 'warning')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'你已成功退出', 'success')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        local_sms = db.session.query(Sms).filter(Sms.id == form.mobile.data).first()
        # print(form.code.data, local_sms.code)
        if int(form.code.data) == local_sms.code:
            print(form.code.data)
            user = User(username=form.username.data, password=form.password.data, mobile=form.mobile.data)
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


@auth.route('/get_sms/<int:mobile>')
def get_sms(mobile):
    # print(session.get('sms_code'))
    # print(g.get('sms_code', None))
    # data = sms(mobile, sms_code)
    # session.setdefault('code', sms_code)
    # session.should_save()
    # print(code)
    # print(session['code'])
    sms_code = random_gen()
    data = sms(mobile, sms_code)
    local_sms = db.session.query(Sms).filter(Sms.id == mobile).first()
    if local_sms is None:
        local_sms = Sms(id=mobile, code=sms_code)
    else:
        local_sms.code = sms_code
    try:
        db.session.add(local_sms)
        db.session.commit()
    except exc:
        db.session.rollback()
        print "%s already exists" % exc
        flash(u"错误,请通知管理员")
    # session['sms_code'] = sms_code
    # if 'sms_code' in session:
    #     print(session['sms_code'])
    return jsonify({'data': data})


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)
