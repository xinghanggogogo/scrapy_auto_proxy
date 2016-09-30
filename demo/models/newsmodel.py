# -*- coding: utf-8 -*-

__author__ = 'xinghang'
#真正的数据库映射文件，这里用来建立数据库的数据结构。
#这里有多个class对应数据库中多个表，类名可以相同，表名不可以相同。
#
from peewee import *

from demo.models.mysql import BaseModel, mysql_db



class newsmodel(BaseModel):
    postId = CharField (null=True)
    title = CharField(null=True)
    description = TextField(null=True)
    author = CharField(null=True)
    classs =  CharField(null=True)
    datetime = CharField(null=True)

    md5 = CharField(null=True,unique=True)
    create_time = DateTimeField(null=True)
    update_time = DateTimeField(null=True)
    link = CharField(null=True)
    source = CharField(null=True)

    postId36kr = CharField (null=True)

    flag = IntegerField(null=True,default=0)
    product = CharField(null=True,default=None)

    class Meta:
        db_table = 'news'


tables = [newsmodel]  #类名
mysql_db.connect()
mysql_db.create_tables(tables, safe=True)