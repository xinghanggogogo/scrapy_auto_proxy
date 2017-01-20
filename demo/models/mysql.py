# -*- coding: utf-8 -*-
__author__ = 'xinghang'

from peewee import *

mysql_db = MySQLDatabase(
    host='',
    port='',
    database='',
    user="",
    passwd="",
    charset=''
)


class BaseModel(Model):
    class Meta:
        database = mysql_db