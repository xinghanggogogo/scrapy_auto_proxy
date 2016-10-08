# -*- coding: utf-8 -*-

__author__ = 'xinghang'

from peewee import *
from demo.models.mysql import BaseModel, mysql_db

class ebookModel(BaseModel):

    name = CharField (null=True, default='')
    img_url = CharField(null=True, default='')
    author = CharField(null=True, default='')
    key_words = CharField(null=True, default='')
    category = CharField(null=True, default='')
    introduction = CharField(null=True, default='')
    comments= CharField(null=True, default='')
    publication_date = CharField(null=True, default='')
    publisher = CharField(null=True, default='')
    publication_city = CharField(null=True, default='')
    hot_level = CharField(null=True, default='')
    isbn10 = CharField(null=True, default='')
    isbn13 = CharField(null=True, default='')
    link_usual = CharField(null=True, default='')
    link_online = CharField(null=True, default='')
    link_txt = CharField(null=True, default='')
    link_pdf = CharField(null=True, default='')
    link_epub = CharField(null=True, default='')
    link_kindle = CharField(null=True, default='')
    md5 = CharField(null=True,unique=True, default='')#唯一标识
    create_time = DateTimeField(null=True, default='')
    update_time = DateTimeField(null=True, default='')

    class Meta:
        db_table = 'books_meta'

tables = [ebookModel]
mysql_db.connect()
mysql_db.create_tables(tables, safe=True)