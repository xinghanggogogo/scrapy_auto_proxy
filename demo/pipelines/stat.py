# -*- coding: utf-8 -*-

__author__ = 'xinghang'

urltotal = 0
itemtotal = 0
successitem = 0
failitem = 0
syncitem = 0

def staturltotal():
    global urltotal
    urltotal = urltotal + 1

def geturltotal():
    return urltotal

def statitemtotal():
    global itemtotal
    itemtotal = itemtotal + 1

def getitemtotal():
    return itemtotal


def statsuccessitem():
    global successitem
    successitem = successitem + 1

def getsuccessitem():
    return successitem


def statfailitem():
    global failitem
    failitem = failitem + 1

def getfailitem():
    return failitem

def statsyncitem():
    global syncitem
    syncitem = syncitem+1

def getsyncitem():
    return syncitem