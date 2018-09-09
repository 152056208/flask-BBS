#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/3
from flask import Blueprint,views,render_template,flash,session,redirect,url_for,g
from functools import wraps
from apps.admin.forms import LoginForm,ResetPwdForm,ResetEmailForm
from apps.admin.models import CMSUser
from flask_mail import Message
from flask import request
bp=Blueprint('admin',__name__,url_prefix='/admin')  #此处注意加斜线
import config
from exts import db,mail
from utls.restful_for import *
from utls import captcha as memcaptcha
import string
import random
from apps.admin.models import CMSPermission

@bp.route('/email/')
def email():
    message=Message('李不搭发的',recipients=['1364826576@qq.com',],body='测试')
    mail.send(message)  #注意此处是send
    return 'ok'

def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if config.Admin_id in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('admin.login'))
    return inner    #注意此处返回

@bp.route('/login/',methods=['GET','POST'])     #管理员登陆
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data=form.data
        user=CMSUser.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['pwd']):    #验证成功
            session[config.Admin_id]=data['email']
            if data['remember']==1:
                session.parmanent=True
            return redirect(url_for('admin.index'))
        else:
            flash('密码错误','err')
            return redirect(url_for('admin.login'))
    return render_template('admin/admin_login.html',form=form)


@bp.route('/index/',methods=['GET'])
@login_required     #此处注意将装饰器放在index下
def index():
    return render_template('admin/admin_index.html')

@bp.route('/logout/')   #退出登陆
def logout():
    session.pop(config.Admin_id)
    return redirect(url_for('admin.login'))


@bp.route('/profile/')  #个人信息
def profile():
    return render_template('admin/admin_profile.html')

@bp.route('/resetpwd/',methods=['GET','POST'])     #修改密码
def resetpwd():
    form=ResetPwdForm()
    if form.validate_on_submit():
        data=form.data
        if g.admin_user.check_password(data['oldpwd']):
            g.admin_user.password=data['newpwd']
            db.session.commit()
            flash('密码修改成功,请重新登陆','ok')
            return redirect(url_for('admin.login'))
        else:
            flash('旧密码错误','err')
    return render_template('admin/admin_resetpwd.html',form=form)

@bp.route('/captcha/')
def email_captcha():
    # email=request.args.get('email')
    email='1364826576@qq.com'
    if not email:
        return params_error('请输入邮箱！')
    source=list(string.ascii_letters)   #小写a-z和A-Z的列表
    source.extend([str(x) for x in range(10)])
    captcha=''.join(random.sample(source,6))    #随机取样
    message=Message('李不搭',recipients=[email],body='您的验证码为：%s'%captcha)
    try:
        mail.send(message)
    except:
        return server_error('服务器错误')
    memcaptcha.set(email,captcha)
    print(memcaptcha.get(email))
    return success('发送验证码成功！')


class ResetEmail(views.MethodView):
    def get(self,form=''):
        form=ResetEmailForm()
        return render_template('admin/admin_resetemail.html',form=form)

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.admin_user.email = email
            db.session.commit()
            return success()
        else:
            return params_error('参数错误')

@bp.route('/banners/')  #轮播图
def banners():
    return render_template('admin/admin_banners.html')

@bp.route('/posts/')    #帖子管理
def posts():
    return render_template('admin/admin_posts.html')

@bp.route('/comments/') #评论管理
def comments():
    return render_template('admin/admin_comments.html')

@bp.route('/boards/')   #板块管理
def boards():
    return render_template('admin/admin_boards.html')

@bp.route('/fusers/')   #前台用户管理
def fusers():
    return render_template('admin/admin_fusers.html')

@bp.route('/cusers/')   #论坛用户管理
def cusers():
    return render_template('admin/admin_cusers.html ')

@bp.route('/croles/')   #角色管理
def croles():
    return render_template('admin/admin_croles.html')

@bp.before_request
def before_request():
    if config.Admin_id in session:
        user_id=session.get(config.Admin_id)
        user=CMSUser.query.filter_by(email=user_id).first()

        if user:
            g.admin_user=user

@bp.context_processor
def cms_context_pocessor():
    return {'CMSPermission':CMSPermission}

bp.add_url_rule('/resetemail/',view_func=ResetEmail.as_view('resetemail'))