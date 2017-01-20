# -*- coding: utf-8 -*-

__author__ = 'xinghang'

from demo.models.mysql import *


class bookDao():

    def find_book_by_isbn(self, isbn):
        sql = "select * from ebook WHERE isbn = '%s'" % isbn
        print '**********************mysql：find book**********************'
        res = mysql_db.execute_sql(sql).fetchone()
        yield  res