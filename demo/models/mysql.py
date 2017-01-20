# -*- coding: utf-8 -*-
__author__ = 'xinghang'

from peewee import *

mysql_db = MySQLDatabase(
    host='192.168.0.172',
    port=3308,
    database='myktv',
    user="mombaby",
    passwd="098f6bcd4621d373cade4e832627b4f6",
    charset='utf8'
)


class BaseModel(Model):
    class Meta:
        database = mysql_db