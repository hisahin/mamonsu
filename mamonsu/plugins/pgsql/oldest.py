# -*- coding: utf-8 -*-

from mamonsu.plugins.pgsql.plugin import PgsqlPlugin as Plugin
from .pool import Pooler


class Oldest(Plugin):
    key_xid = 'pgsql.oldest[xid_age]'
    key_time = 'pgsql.oldest[query_time]'

    OldestXidSql = "select greatest(max(age(backend_xmin)), max(age(backend_xid))) from pg_catalog.pg_stat_activity;"

    OldestXidSql_bootstrap = "select public.mamonsu_get_oldest_xid();"

    OldestQuerySql = "select extract(epoch from max(now() - xact_start)) from pg_catalog.pg_stat_activity;"

    OldestQuerySql_bootstrap = "select public.mamonsu_get_oldest_query();"

    DEFAULT_CONFIG = {
        'max_xid_age': str(5000 * 60 * 60),
        'max_query_time': str(5 * 60 * 60)
    }

    def run(self, zbx):
        if Pooler.is_bootstraped() and Pooler.bootstrap_version_greater('2.3.2'):
            xid = Pooler.query(self.OldestXidSql_bootstrap)[0][0]
            query = Pooler.query(self.OldestQuerySql_bootstrap)[0][0]
        else:
            xid = Pooler.query(self.OldestXidSql)[0][0]
            query = Pooler.query(self.OldestQuerySql)[0][0]

        zbx.send(self.key_xid, xid)
        zbx.send(self.key_time, query)

    def graphs(self, template):
        result = template.graph({
            'name': 'PostgreSQL oldest query running time',
            'items': [{
                'key': self.key_time,
                'color': '00CC00'
            }]
        })
        result += template.graph({
            'name': 'PostgreSQL age of oldest xid',
            'items': [{
                'key': self.key_xid,
                'color': '00CC00'
            }]
        })
        return result

    def items(self, template):
        return template.item({
            'key': self.key_xid,
            'name': 'PostgreSQL: age of oldest xid',
            'value_type': Plugin.VALUE_TYPE.numeric_unsigned
        }) + template.item({
            'key': self.key_time,
            'name': 'PostgreSQL: oldest query running time in sec',
            'units': Plugin.UNITS.s
        })

    def triggers(self, template):
        return template.trigger({
            'name': 'PostgreSQL oldest xid is too big on {HOSTNAME}',
            'expression': '{#TEMPLATE:pgsql.oldest[xid_age]'
                          '.last()}&gt;' + self.plugin_config('max_xid_age')
        }) + template.trigger({
            'name': 'PostgreSQL query running is too old on {HOSTNAME}',
            'expression': '{#TEMPLATE:pgsql.oldest[query_time]'
                          '.last()}&gt;' + self.plugin_config('max_query_time')
        })

    def keys_and_queries(self, template_zabbix):
        result = []
        result.append(['{0},"{1}"'.format(self.key_time, self.OldestQuerySql)])
        result.append(['{0},"{1}"'.format(self.key_xid,  self.OldestXidSql )])
        return template_zabbix.key_and_query(result)
