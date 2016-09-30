# -*- coding: utf-8 -*-
'''
数据库的操作文件
1.倒入数据库的连接文件：leiyun.models.musql_qxxy
2.LieyunDao驼峰命名法，实现对数据库中某个表的操作，这里取出min（post_date）并返回

'''
__author__ = 'xinghang'
from demo.models.mysql import *

class bookDao():
    def find_book_by_isbn(self, isbn):
        sql = "select * from ebook WHERE isbn = '%s'" % isbn
        print '**********************mysql：find book**********************'
        res = mysql_db.execute_sql(sql).fetchone()
        yield  res