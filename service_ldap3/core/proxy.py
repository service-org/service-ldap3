#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import logging
import typing as t

from ldap3 import NTLM
from ldap3 import Server
from ldap3 import Connection
from ldap3 import ServerPool
from ldap3.utils.log import NETWORK
from service_core.core.configure import Configure
from service_ldap3.constants import LDAP3_CONFIG_KEY
from ldap3.utils.log import set_library_log_detail_level
from ldap3.utils.log import set_library_log_activation_level


class LdapProxy(object):
    """ Ldap代理类 """

    def __init__(
            self,
            config: Configure,
            debug: bool = False,
            srvlist_options: t.Optional[t.List[t.Dict[t.Text, t.Any]]] = None,
            srvpool_options: t.Optional[t.Dict[t.Text, t.Any]] = None,
            connect_options: t.Optional[t.Dict[t.Text, t.Any]] = None
    ) -> None:
        """ 初始化实例

        @param config: 配置对象
        @param debug: 开启调试
        @param srvlist_options: 实例配置
        @param srvpool_options: 池子配置
        @param connect_options: 连接配置
        """
        self.config = config
        self.debug = debug
        self.client = None
        self.srvlist_options = srvlist_options or []
        self.srvpool_options = srvpool_options or {}
        self.connect_options = connect_options or {}
        debug and set_library_log_detail_level(NETWORK)
        debug and set_library_log_activation_level(logging.DEBUG)

    def __call__(
            self,
            alias: t.Text,
            debug: bool = False,
            srvlist_options: t.Optional[t.List[t.Dict[t.Text, t.Any]]] = None,
            srvpool_options: t.Optional[t.Dict[t.Text, t.Any]] = None,
            connect_options: t.Optional[t.Dict[t.Text, t.Any]] = None
    ) -> Connection:
        """ 代理可调用

        @param alias: 配置别名
        @param debug: 开启调试
        @param srvlist_options: 实例配置
        @param srvpool_options: 池子配置
        @param connect_options: 连接配置
        """
        debug = debug or self.debug
        debug and set_library_log_detail_level(NETWORK)
        debug and set_library_log_activation_level(logging.DEBUG)
        srvlist_options = self.config.get(f'{LDAP3_CONFIG_KEY}.{alias}.srvlist_options', default=[])
        # 防止YAML中声明值为None
        self.srvlist_options += (srvlist_options or [])
        srvpool_options = self.config.get(f'{LDAP3_CONFIG_KEY}.{alias}.srvpool_options', default={})
        # 防止YAML中声明值为None
        self.srvpool_options = (srvpool_options or {}) | self.srvpool_options
        self.srvpool_options.setdefault('servers', None)
        self.server_pool = ServerPool(**self.srvpool_options)
        for server_options in self.srvlist_options: self.server_pool.add(Server(**server_options))
        connect_options = self.config.get(f'{LDAP3_CONFIG_KEY}.{alias}.connect_options', default={})
        # 防止YAML中声明值为None
        self.connect_options = (connect_options or {}) | self.connect_options
        self.connect_options.setdefault('server', self.server_pool)
        self.connect_options.setdefault('auto_bind', True)
        self.connect_options.setdefault('authentication', NTLM)
        self.connect_options.setdefault('pool_size', len(self.srvlist_options))
        self.client = self.client or Connection(**self.connect_options)
        return self.client
