#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from ldap3 import Connection as BaseConnection


class Connection(BaseConnection):
    """ Ldap通用连接类 """
    pass
