# coding=utf-8
# __author__ = 'tk'
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, Regexp, EqualTo, DataRequired
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'保持登录')
    submit = SubmitField(u'登录')


class RegistrationForm(Form):
    username = StringField(u'用户名', validators=[
        DataRequired(u'请输入用户名'), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名以字母开头+字母或数字或下划线')])
    password = PasswordField(u'密码', validators=[
        DataRequired(u'请输入密码'), EqualTo('password2', message=u'请确认密码')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired(u'请确认密码')])
    mobile = StringField(u'手机号', validators=[DataRequired(u'请输入手机号'),
                                             Regexp('^(1(3|5|7|8)[0-9]{9})$', 0, u'输入正确的手机号')])
    code = StringField(u'验证码', validators=[DataRequired(u'六位验证码'), Regexp('[0-9]*'), Length(6, 6)])
    submit = SubmitField(u'注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名重复')
