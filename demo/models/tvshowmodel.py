# -*- coding: utf-8 -*-

__author__ = 'xinghang'

from peewee import *
from demo.models.mysql import BaseModel, mysql_db

class tvshowModel(BaseModel):

    show_img = CharField (null=True)
    link = CharField(null=True)
    video_link = CharField(null=True)
    title = CharField(null=True)
    anchor =  CharField(null=True)
    category = CharField(null=True)
    head_img = CharField(null=True)
    num = CharField(null=True)
    room_id = CharField(null=True)
    source = CharField(null=True)

    md5 = CharField(null=True,unique=True)
    create_time = DateTimeField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        db_table = 'tvshow'

tables = [tvshowModel]
mysql_db.connect()
mysql_db.create_tables(tables, safe=True)
