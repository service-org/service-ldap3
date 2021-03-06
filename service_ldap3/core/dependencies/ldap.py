#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from ldap3 import NTLM
from ldap3 import Server
from ldap3 import ServerPool
from ldap3 import RESTARTABLE
from logging import getLogger
from service_ldap3.core.client import LdapClient
from service_ldap3.constants import LDAP3_CONFIG_KEY

from service_core.core.service.dependency import Dependency

logger = getLogger(__name__)


class Ldap(Dependency):
    """ Ldap依赖类

    doc: https://ldap3.readthedocs.io/en/latest/index.html
    """

    name = 'Ldap'

    def __init__(
            self,
            alias: t.Text,
            srvlist_options: t.Optional[t.List[t.Dict[t.Text, t.Any]]] = None,
            srvpool_options: t.Optional[t.Dict[t.Text, t.Any]] = None,
            connect_options: t.Optional[t.Dict[t.Text, t.Any]] = None,
            **kwargs: t.Any
    ) -> None:
        """ 初始化实例

        @param alias: 配置别名
        @param srvlist_options: 实例配置
        @param srvpool_options: 池子配置
        @param connect_options: 连接配置
        """
        self.alias = alias
        self.client = None
        self.srvlist_options = srvlist_options or []
        self.srvpool_options = srvpool_options or {}
        self.connect_options = connect_options or {}
        super(Ldap, self).__init__(**kwargs)

    def setup(self) -> None:
        """ 声明周期 - 载入阶段 """
        srvlist_options = self.container.config.get(f'{LDAP3_CONFIG_KEY}.{self.alias}.srvlist_options', default=[])
        # 防止YAML中声明值为None
        self.srvlist_options += (srvlist_options or [])
        srvpool_options = self.container.config.get(f'{LDAP3_CONFIG_KEY}.{self.alias}.srvpool_options', default={})
        # 防止YAML中声明值为None
        self.srvpool_options = (srvpool_options or {}) | self.srvpool_options
        self.srvpool_options.update({'servers': None})
        server_pool = ServerPool(**self.srvpool_options)
        for server_options in self.srvlist_options: server_pool.add(Server(**server_options))
        connect_options = self.container.config.get(f'{LDAP3_CONFIG_KEY}.{self.alias}.connect_options', default={})
        # 防止YAML中声明值为None
        self.connect_options = (connect_options or {}) | self.connect_options
        self.connect_options.setdefault('auto_bind', True)
        self.connect_options.update({'server': server_pool})
        self.connect_options.setdefault('authentication', NTLM)
        # 开启心跳防止服务端断开
        self.connect_options.setdefault('pool_keepalive', 60)
        self.connect_options.setdefault('pool_lifetime', 3600)
        self.connect_options.setdefault('client_strategy', RESTARTABLE)
        self.connect_options.setdefault('pool_size', len(self.srvlist_options))
        self.client = LdapClient(**self.connect_options)

    def stop(self) -> None:
        """ 声明周期 - 关闭阶段

        @return: None
        """
        self.client and self.client.unbind()

    def get_instance(self) -> LdapClient:
        """ 获取注入对象

        @return: LdapClient
        """
        return self.client
