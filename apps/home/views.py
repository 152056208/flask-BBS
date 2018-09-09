#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/3
from flask import Blueprint
bp=Blueprint('home',__name__)

@bp.route('/')
def index():
    return 'home'