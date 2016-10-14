# -*- coding: utf-8 -*-

__author__ = 'xinghang'

from peewee import *
from demo.models.mysql import BaseModel, mysql_db

class proxymodel(BaseModel):

    ip = CharField (null=True)
    port = CharField(null=True)

    md5 = CharField(null=True,unique=True)
    create_time = DateTimeField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        db_table = 'proxy'

tables = [proxymodel]
mysql_db.connect()
mysql_db.create_tables(tables, safe=True)