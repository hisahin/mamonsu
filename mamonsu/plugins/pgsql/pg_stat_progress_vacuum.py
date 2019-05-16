from mamonsu.plugins.pgsql.plugin import PgsqlPlugin as Plugin
from .pool import Pooler


class PgStatProgressVacuum(Plugin):

    DEFAULT_CONFIG = {'max_index_vacuum_count': str(0)}
    AgentPluginType = 'pg'
    query = """select count(c.relname) from pg_stat_progress_vacuum v inner join pg_class c on v.relid = c.oid"""
    query_agent = """select count({0}) from pg_stat_progress_vacuum v inner join pg_class c on v.relid = c.oid;"""
    key = 'pgsql.pg_stat_progress_vacuum{0}'
    Items = [
        # key, desc, color
        ('index_vacuum_count',
         'index_vacuum_count of the vacuum',
         '0000CC')
    ]

    def run(self, zbx):
        result = Pooler.query(self.query)
        for item in self.Items:
           # found = False
            for row in result:
                #if row[0] == '{0}'.format(item[0]): #
                    #found = True
                    zbx.send('{0}[{1}]'.format('pgsql.pg_stat_progress_vacuum', item[0]), row[0])
                ## if row[i] is the same as data from select send it with data (from result)
            #if not found:
              #  zbx.send('pgsql.pg_stat_progress_vacuum[{0}]'.format(item[0]), 99) # if where is no data

    def items(self, template):
        result = ''
        for item in self.Items:
            result += template.item({
                'key': self.right_type(self.key, item[0]),
                'name': 'PostgreSQL vacuum: {0}'.format(item[1]),
                'value_type': self.VALUE_TYPE.numeric_unsigned
            })
        return result

    def graphs(self, template):
        name, items = 'PostgreSQL VACUUM', []
        for item in self.Items:
            items.append({
                'key': self.right_type(self.key, item[0]),
                'color': item[2]
            })
        return template.graph({'name': name, 'items': items})

    def triggers(self, template):
        return template.trigger({
            'name': 'PostgreSQL count tables where index_vacuum_count is more than 1 on {HOSTNAME}',
            'expression': '{#TEMPLATE:' + self.right_type(self.key, self.Items[0][0]) +
                          '.last()}&gt;' + self.plugin_config('max_index_vacuum_count')
        })

    def keys_and_queries(self, template_zabbix):
        result = []
        for i, item in enumerate(self.Items):
                result.append('{0}[*],$2 $1 -c "{1}"'.format(self.key.format('.'+item[0]), self.query_agent.format(item[0])))
        return template_zabbix.key_and_query(result)

    def sql(self):
        result = {}  # key is name of file, var is query
        for i, item in enumerate(self.Items):
            result[self.key.format('.' + item[0])] = self.query_agent.format(item[0])
        return result

