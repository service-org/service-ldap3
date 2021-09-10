#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_ldap3.core.proxy import LdapProxy
from service_core.cli.subctxs import BaseContext
from service_core.core.configure import Configure


class Ldap(BaseContext):
    """ 用于调试Ldap接口 """

    name: t.Text = 'ldap'

    def __init__(self, config: Configure) -> None:
        """ 初始化实例

        @param config: 配置对象
        """
        super(Ldap, self).__init__(config)
        self.proxy = LdapProxy(config=config)
