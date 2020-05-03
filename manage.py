#!/usr/bin/python 
# -*- coding: utf-8 -*-


from flask import current_app
from src import create_app
from src.misc.exts import db
from src.models import Project
from flask_script import Manager, Server, Shell

manager = Manager(create_app)
server = Server(host='0.0.0.0', port=15942, use_debugger=True)


def make_shell_context():
    return dict(
        app=current_app,
        db=db,
        Project=Project,
    )


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', server)


def dadd(inputs):
    for i in inputs:
        db.session.add(i)
    db.session.commit()

@manager.command
def createdb():
    print ('开始创建数据库')
    db.create_all()
    print('创建数据库成功')
    print('开始初始化数据')

    # 固有配置

    project1 = Project(
        name='萌推', description='电商项目', logo='http://tcloud-static.ywopt.com/static/468e0de0-8c92-4843-b456-2751208a44e4.png'
    )
    project2 = Project(
        name='实惠喵', description='返利网',logo='http://tcloud-static.ywopt.com/static/6d2600e1-4928-4168-893d-00548460dd3f.png'
    )
    dadd([project1,project2])
    print('数据初始化完成')

@manager.command
def dropdb():
    print('开始删除数据库')
    db.drop_all()
    print('数据库删除完成')

@manager.command
def initdb():
    dropdb()
    createdb()

if __name__ == '__main__':
    manager.run()
