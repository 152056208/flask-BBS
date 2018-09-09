#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/3
from wtforms import StringField,IntegerField,SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError
from utls import captcha as memcache
from utls.restful_for import *
from flask import g

class LoginForm(FlaskForm):
    email=StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱!')
        ],
        description='邮箱',
        render_kw={
            'class':"form-control",
            'placeholder':"请输入邮箱",
            'required':'required'
        }
    )
    pwd=StringField(
        label='密码',
        validators=[
            DataRequired('请输入密码!')
        ],
        description='密码',
        render_kw={
            'class':"form-control",
            'placeholder':"密码",
            'required':'required'
        }
    )
    submit=SubmitField(
        label='登陆',
        render_kw={
            'class':"btn btn-lg btn-primary btn-block" ,
            'type':"submit"
        }
    )
    remember=IntegerField(
        label='记住密码',
        description='记住密码',
         render_kw={
            'type':"checkbox"
        }
    )

class ResetPwdForm(FlaskForm):
    oldpwd=StringField(
        label='旧密码',
        description='旧密码',
        validators=[Length(4,10,message='请输入4-10位长的密码！')],
        render_kw={
            'class':"form-control"  ,'placeholder':"请输入旧密码"
        }
    )
    newpwd=StringField(
        label='新密码',
        description='新密码',
        validators=[Length(4,10,message='请输入4-10位长的密码！')],
        render_kw={
            'class':"form-control"  ,'placeholder':"请输入新密码",'required':'required'
        }
    )
    newpwd2=StringField(
        label='确认密码',
        description='确认密码',
        validators=[EqualTo('newpwd',message='两次输入的密码不一致'),],   #此处注意将值括起来
        render_kw={
            'class':"form-control" ,'placeholder':"请再次输入密码",'required':'required'
        }
    )
    submit=SubmitField(
        label='确认修改',
        render_kw={
            'class':"btn btn-lg btn-block" ,
            'type':"submit"
        }
    )

# class ResetEmail(FlaskForm):
#     email=StringField(
#         label='新邮箱',
#         description='新邮箱',
#         validators=[Email(message='请输入正确的邮箱格式')],   #此处注意将值括起来
#         render_kw={
#             'type':"email", 'placeholder':"新邮箱" ,'class':"form-control",'required':'required'
#         }
#     )
#     captcha=StringField(
#         label='验证码',
#         validators=[Length(6,6,message='请输入正确的验证码！')],
#         render_kw={
#            'type':"text",'placeholder':"邮箱验证码" ,'class':"form-control",'required':'required'
#         }
#     )
#     submit=SubmitField(
#         label='立即修改',
#         render_kw={
#             'class':"btn btn-lg btn-block" ,
#             'type':"submit",'required':'required'
#         }
#     )
#
#     #验证码
#     def validate_captcha(self,field):
#         captch=field.data
#         print(captcha.cache.get('email'))
#         email=self.email
#         print(email)
#         # captcha_cache=captcha.get(email)
#         # if not captcha_cache or captch.lower() != captcha_cache.lower():
#         #     return params_error('验证码错误!')
#
#     def validate_email(self,field):
#         email=field.data
#         user=g.admin_user
#         if user.email==email:
#             raise ValidationError('验证邮箱不能为当前邮箱！')

# class ResetpwdForm(FlaskForm):
#     oldpwd = StringField(validators=[Length(6,20,message="请输入正确格式的旧密码")])
#     newpwd = StringField(validators=[Length(6,20,message="请输入正确格式的新密码")])
#     newpwd2 = StringField(validators=[EqualTo('newpwd',message="两次输入的密码不一致")])


class ResetEmailForm(FlaskForm):
    email = StringField(validators=[Email(message="请输入正确格式的邮箱")])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入正确的邮箱验证码')])
    # 自定义验证
    def validate_captcha(self,field):
        #form要提交的验证码和邮箱
        captcha = field.data
        email = self.email.data
        #缓存里面保存的邮箱对应的验证码
        print(email)
        if email:
            captcha_cache =memcache.get(email)
            print(captcha_cache)
            #如果缓存中没有这个验证码，或者缓存中的验证码跟form提交的验证码不相等（不区分大小写）
            # 两个有一个不成立，就抛异常
            if not captcha_cache or captcha.lower() != captcha_cache.lower():
                raise ValidationError('邮箱验证码错误!')

    def validate_email(self, field):
        email = field.data
        user = g.admin_user
        if user.email == email:
            raise ValidationError('不能修改为当前使用的邮箱！')
