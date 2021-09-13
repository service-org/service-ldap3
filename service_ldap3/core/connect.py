#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from ldap3 import Connection as BaseConnection


class Connection(BaseConnection):
    """ Ldap3通用连接 """

    def __init__(self, *args: t.Any, base_dn: t.Optional[t.Text] = None, **kwargs: t.Text) -> None:
        """ 初始化实例

        @param base_dn:根域名称
        @param args  : 位置参数
        @param kwargs: 命名选项
        """
        self.base_dn = base_dn or ''
        super(Connection, self).__init__(*args, **kwargs)
