# 运行环境

|system |python | 
|:------|:------|      
|cross platform |3.9.16|

# 组件安装

```shell
pip install -U service-ldap3 
```

# 服务配置

> config.yaml

```yaml
CONTEXT:
  - service_ldap3.cli.subctxs.ldap:Ldap
LDAP3:
  test:
    srvlist_options:
      - host: ldaps://127.0.0.1:636
    connect_options:
      user: cn\test
      password: test
```

# 入门案例

```yaml
├── config.yaml
├── facade.py
└── project
    ├── __init__.py
    └── service.py
```

> service.py

```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from logging import getLogger
from ldap3 import Connection as LdapConnection
from service_ldap3.core.dependencies import Ldap
from service_croniter.core.entrypoints import croniter
from service_core.core.service import Service as BaseService

logger = getLogger(__name__)


class Service(BaseService):
    """ 微服务类 """

    # 微服务名称
    name = 'demo'
    # 微服务简介
    desc = 'demo'

    # 作为依赖项
    ad: LdapConnection = Ldap(alias='test')

    @croniter.cron('* * * * * */1')
    def test_ldap_whoami(self) -> None:
        """ 测试LDAP whoami命令

        doc: https://ldap3.readthedocs.io/en/latest/
        @return: None
        """
        me = self.ad.extend.standard.who_am_i()
        logger.debug(f'yeah~ yeah~ yeah~, i am {me}')
```

> facade.py

```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from project import Service

service = Service()
```

# 运行服务

> core start facade --debug

# 接口调试

> core shell --shell `shell`

```shell
* eventlet 0.31.1
    - platform: macOS 10.15.7
      error  : changelist must be an iterable of select.kevent objects
      issue  : https://github.com/eventlet/eventlet/issues/670#issuecomment-735488189
    - platform: macOS 10.15.7
      error  : monkey_patch causes issues with dns .local #694
      issue  : https://github.com/eventlet/eventlet/issues/694#issuecomment-806100692

2021-09-10 17:34:28,412 - 61412 - DEBUG - load subcmd service_core.cli.subcmds.shell:Shell succ
2021-09-10 17:34:28,417 - 61412 - DEBUG - load subcmd service_core.cli.subcmds.debug:Debug succ
2021-09-10 17:34:28,419 - 61412 - DEBUG - load subcmd service_core.cli.subcmds.start:Start succ
2021-09-10 17:34:28,419 - 61412 - DEBUG - load subcmd service_core.cli.subcmds.config:Config succ
2021-09-10 17:34:28,644 - 61412 - DEBUG - load subctx service_core.cli.subctxs.config:Config succ
2021-09-10 17:34:28,644 - 61412 - DEBUG - load subctx service_ldap3.cli.subctxs.ldap:Ldap succ
CPython - 3.9.6 (tags/v3.9.6:db3ff76, Jun 28 2021, 15:26:21) [MSC v.1929 64 bit (AMD64)]
>>> s.ldap.proxy(alias='test').extend.standard.who_am_i()
'u:CN\\test'
```

# 运行调试

> core debug --port `port`
