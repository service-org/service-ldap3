#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import logging
import typing as t

from ldap3 import Connection
from ldap3.utils.log import NETWORK
from ldap3.utils.log import set_library_log_detail_level
from ldap3.utils.log import set_library_log_activation_level


class LdapClient(Connection):
    """ Ldap3通用连接类 """

    def __init__(
            self,
            *args: t.Any,
            debug: t.Optional[bool] = None,
            base_dn: t.Optional[t.Text] = None,
            **kwargs: t.Text
    ) -> None:
        """ 初始化实例

        @param debug : 开启调试
        @param base_dn:根域名称
        @param args  : 位置参数
        @param kwargs: 命名选项
        """
        self.base_dn = base_dn or ''
        debug and set_library_log_detail_level(NETWORK)
        debug and set_library_log_activation_level(logging.DEBUG)
        super(LdapClient, self).__init__(*args, **kwargs)
