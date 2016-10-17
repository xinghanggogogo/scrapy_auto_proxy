# -*- coding: utf-8 -*-

__author__ = 'xinghang'

from peewee import *
from demo.models.mysql import BaseModel, mysql_db

class bookcommentModel(BaseModel):

    book_name = CharField (null=True, default='')
    title = CharField(null=True, default='')
    time = CharField(null=True, default='')
    content= CharField(null=True, default='')

    md5 = CharField(null=True,unique=True, default='')
    create_time = DateTimeField(null=True, default='')
    update_time = DateTimeField(null=True, default='')

    class Meta:
        db_table = 'bookscomment'

tables = [bookcommentModel]
mysql_db.connect()
mysql_db.create_tables(tables, safe=True)