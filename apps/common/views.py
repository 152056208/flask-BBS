#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/3
from flask import Blueprint
bp=Blueprint('common',__name__,url_prefix='/c')  #此处注意加斜线

@bp.route('/')
def index():
    return 'common'