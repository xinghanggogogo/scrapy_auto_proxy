# -*- coding: utf-8 -*-

__author__ = 'xinghang'

from peewee import *
from demo.models.mysql import BaseModel, mysql_db

class namemodel(BaseModel):

    gender = CharField (null=True)
    ename = CharField(null=True)
    sounce = CharField(null=True)
    cname =  CharField(null=True)
    source = CharField(null=True)
    charactors = CharField(null=True)
    hot_level = CharField(null=True)
    detail = CharField(null=True)
    detail_link = CharField(null=True)
    masters = CharField(null=True)

    md5 = CharField(null=True,unique=True)
    create_time = DateTimeField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        db_table = 'namegame'

tables = [namemodel]
mysql_db.connect()
mysql_db.create_tables(tables, safe=True)