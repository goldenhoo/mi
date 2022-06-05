from wtforms_tornado import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Length


class UserForm(Form):
    username = StringField('账号', validators=[Length(min=11, max=11, message='请正确填写手机号')])
    password = StringField('密码', validators=[Length(min=6, message='请正确填写密码')])


class LoginUserForm(Form):
    username = StringField('账号', validators=[DataRequired(message='请正确填写手机号')])
    password = StringField('密码', validators=[Length(min=6, message='请正确填写密码')])
