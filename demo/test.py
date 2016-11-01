# -*- coding: utf-8 -*-

# str = 'Tasdf&-asdF'
# print str.lower()

# class Info(object):
#     def __init__(self):
#         self.__name = 'jay'
#     def __say(self):
#         print self.__name
#     def say(self):
#         print self.__name
#
# a = Info()
# print a.__name

# -*-coding:utf-8-*-

# import uuid
# import urllib2
# import cookielib
# import os
#
# '''获取文件后缀名'''
# def get_file_extension(file):
#     return os.path.splitext(file)[1]
#
#
# '''創建文件目录，并返回该目录'''
# def mkdir(path):
#     # 去除左右两边的空格
#     path = path.strip()
#     # 去除尾部 \符号
#     path = path.rstrip("\\")
#
#     if not os.path.exists(path):
#         os.makedirs(path)
#
#     return path
#
#
# '''自动生成一个唯一的字符串，固定长度为36'''
# def unique_str():
#     return str(uuid.uuid1())
#
# '''
# 抓取网页文件内容，保存到内存
# @url 欲抓取文件 ，path+filename
# '''
# def get_file(url):
#     try:
#         cj = cookielib.LWPCookieJar()
#         opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#         urllib2.install_opener(opener)
#
#         req = urllib2.Request(url)
#         operate = opener.open(req)
#         data = operate.read()
#         return data
#     except BaseException, e:
#         print e
#         return None
#
#
# '''
# 保存文件到本地
# @path  本地路径
# @file_name 文件名
# @data 文件内容
# '''
# def save_file(path, file_name, data):
#     if data == None:
#         return
#
#     mkdir(path)
#     if (not path.endswith("/")):
#         path = path + "/"
#     file = open(path + file_name, "wb")
#     file.write(data)
#     file.flush()
#     file.close()
#
#
# # 获取文件后缀名
# print get_file_extension("123.jpg");
# # 創建文件目录，并返回该目录
# # print mkdir("d:/ljq")
# # 自动生成一个唯一的字符串，固定长度为36
# print unique_str()
#
# url = "http://qlogo1.store.qq.com/qzone/416501600/416501600/100?0";
# save_file("d:/ljq/", "123.jpg", get_file(url))
#
# #coding:utf-8
# from bs4 import BeautifulSoup
#
# import requests
# import re
# import urllib
#
# DownPath = "/jiaoben/python/meizitu/pic/"
# head = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
# TimeOut = 5
# PhotoName = 0
# c = '.jpeg'
# PWD="/jiaoben/python/meizitu/pic/"
#
# for x in range(1,4):
#   site = "http://www.meizitu.com/a/qingchun_3_%d.html" %x
#   Page = requests.session().get(site,headers=head,timeout=TimeOut)
#   Coding =  (Page.encoding)
#   Content = Page.content#.decode(Coding).encode('utf-8')
#   ContentSoup = BeautifulSoup(Content)
#   jpg = ContentSoup.find_all('img',{'class':'scrollLoading'})
#   for photo in jpg:
#     PhotoAdd = photo.get('data-original')
#     PhotoName +=1
#     Name =  (str(PhotoName)+c)
#     r = requests.get(PhotoAdd,stream=True)
#     with open(PWD+Name, 'wb') as fd:
#         for chunk in r.iter_content():
#                 fd.write(chunk)
# print ("You have down %d photos" %PhotoName)

# import urllib2
# import cookielib
#
# cookie = cookielib.CookieJar()
# handler=urllib2.HTTPCookieProcessor(cookie)
# opener = urllib2.build_opener(handler)
# response = opener.open('http://www.baidu.com')
#
# for item in cookie:
#     print 'Name = '+item.name
#     print 'Value = '+item.value

# import urllib
# import urllib2
# import cookielib
#
# filename = 'cookie.txt'
# cookie = cookielib.MozillaCookieJar(filename)
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
# postdata = urllib.urlencode({
# 			'stuid':'201200131012',
# 			'pwd':'23342321'
# 		})
# #
# loginUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bks_login2.login'
# result = opener.open(loginUrl,postdata)
# cookie.save(ignore_discard=True, ignore_expires=True)
# #利用cookie请求访问另一个网址，此网址是成绩查询网址
# gradeUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bkscjcx.curscopre'
# #请求访问成绩查询网址
# result = opener.open(gradeUrl)
# print result.read()
#
# str = 'asdf'
# print str[-3:-1]

str = 'asdf'
if str:
	print 'asdfasdf'