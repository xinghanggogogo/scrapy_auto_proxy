# -*- coding: utf-8 -*-

__author__ = 'xinghang'
from peewee import *
from demo.models.mysql import BaseModel, mysql_db



class cardmodel(BaseModel):
    icon = CharField (null=True)
    name = CharField(null=True)
    description = CharField(null=True)
    classs =  CharField(null=True)
    source = CharField(null=True)
    datetime = CharField(null=True)
    locallink = CharField(null=True)
    link = CharField(null=True)

    md5 = CharField(null=True,unique=True)
    create_time = DateTimeField(null=True)
    update_time = DateTimeField(null=True)


    class Meta:
        db_table = 'carditem'


tables = [cardmodel]  #类名
mysql_db.connect()
mysql_db.create_tables(tables, safe=True)