#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/3
from flask_script import Manager
from flask_migrate import  Migrate,MigrateCommand
from exts import db
from myflaskbbs import create_app
from apps.admin.models import CMSUser,CMSPermission,CMSRole

app=create_app()

manager=Manager(app)

Migrate(app,db)   #绑定app跟db
manager.add_command('db',MigrateCommand)


admin_user=CMSUser
@manager.option('-u','--username')
@manager.option('-p','--password')
@manager.option('-e','--email')
def create_cms_user(username,password,email):
    user=admin_user(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('添加用户成功')

@manager.command
def create_role():
    '''创建角色'''
    # 1.访问者（可以修改个人信息）
    visitor = CMSRole(name='访问者',desc='只能访问数据，不能修改')
    visitor.permissions = CMSPermission.VISITOR

    # 2.运营人员（修改个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='运营',desc='管理帖子，管理评论，管理前台用户,')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER\
                           |CMSPermission.CMSUSER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER

    # 3.管理员（拥有所有权限）
    admin = CMSRole(name='管理员',desc='拥有本系统所有权限')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.CMSUSER\
                        |CMSPermission.COMMENTER|CMSPermission.FRONTUSER|CMSPermission.BOARDER

    # 4.开发者
    developer = CMSRole(name='开发者',desc='开发人员专用角色')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()


@manager.option('-e','--email',dest='email')     #用户邮箱
@manager.option('-n','--name',dest='name')       #角色名字
def add_user_to_role(email,name):
    '''添加用户到某个角色'''
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            #把用户添加到角色里面
            role.users.append(user)
            db.session.commit()
            print("用户添加到角色成功!")
        else:
            print("没有这个角色：%s" %role)
    else:
        print("%s邮箱没有这个用户!"%email)


if __name__=='__main__':
    manager.run()