#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-12
'''''
pyspider结果保存到数据库简单样例。
使用方法：
    1, 把本文件放到pyspider/pyspider/database/mysql/目录下命名为mysqldb.py;
    2, 建立相应的表和库;
    3, 在脚本文件里使用from pyspider.database.mysql.mysqldb import ToMysql引用本代码;
    4, 重写on_result方法.
'''
from six import itervalues
import MySQLdb


class ToMysql():
    def __init__(self):

        kwargs = {  'host':'192.168.0.172',
                    'port':3308,
                    'user':'mombaby',
                    'passwd':'098f6bcd4621d373cade4e832627b4f6',
                    'db':'myktv',
                    'charset':'utf8'}

        hosts = kwargs['host']
        username = kwargs['user']
        port = kwargs['port']
        password = kwargs['passwd']
        database = kwargs['db']
        charsets = kwargs['charset']

        self.connection = False
        try:
            self.conn = MySQLdb.connect(host=hosts, port=port, user=username, passwd=password, db=database, charset=charsets)
            self.cursor = self.conn.cursor()
            self.cursor.execute("set names " + charsets)
            self.connection = True
        except Exception, e:
            print "Cannot Connect To Mysql!/n", e

    def escape(self, string):
        return '%s' % string

    def into(self, tablename='tvshow', **values):

        if self.connection:

            tablename = self.escape(tablename)
            print '******begin test exist******'
            test_sql = "select * from %s where anchor = '%s'" % (tablename, values['anchor'])
            exist_info = self.cursor.execute(test_sql)
            if exist_info:
                print '******记录已经存在******'
                sql_query = "update %s set show_img='%s', m3u8_link='%s', title='%s', num='%s' where anchor = '%s'" % (tablename, values['show_img'], values['m3u8_link'], values['title'], values['num'], values['anchor'])
            else:
                print '******记录不存在,首次插入******'
                _keys = ",".join(self.escape(k) for k in values)
                _values = ",".join(['%s', ] * len(values))
                sql_query = "insert into %s (%s) values (%s)" % (tablename, _keys, _values)

            try:
                if not exist_info:
                    self.cursor.execute(sql_query, list(itervalues(values)))
                    print "******首次插入成功******"
                else:
                    self.cursor.execute(sql_query)
                    print "******更新成功******"
                self.conn.commit()
                return True

            except Exception, e:
                print "An Error Occured: ", e
                return False

    def into_issue(self, tablename='hotissue', **values):

        if self.connection:

            tablename = self.escape(tablename)

            _keys = ",".join(self.escape(k) for k in values)
            _values = ",".join(['%s', ] * len(values))
            sql_query = "insert into %s (%s) values (%s)" % (tablename, _keys, _values)

            try:
                self.cursor.execute(sql_query, list(itervalues(values)))
                print "******首次插入成功******"
                self.conn.commit()
                return True

            except Exception, e:
                print "记录已经存在: ", e
                return False


        # if self.connection:
        #     tablename = self.escape(tablename)
        #     if values:
        #         _keys = ",".join(self.escape(k) for k in values)
        #         _values = ",".join(['%s', ] * len(values))
        #         sql_query = "insert into %s (%s) values (%s)" % (tablename, _keys, _values)
        #     else:
        #         sql_query = "replace into %s default values" % tablename
        #     try:
        #         if values:
        #             self.cursor.execute(sql_query, list(itervalues(values)))
        #         else:
        #             self.cursor.execute(sql_query)
        #         self.conn.commit()
        #         return True
        #     except Exception, e:
        #         print "An Error Occured: ", e
        #         return False
