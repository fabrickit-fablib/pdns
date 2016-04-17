# coding: utf-8

from fabkit import run, filer, sudo, env
from fablib.base import SimpleBase


class PDNS(SimpleBase):
    def __init__(self):
        self.data_key = 'pdns'
        self.data = {
            'is_master': False,
            'is_slave': False,
        }

        self.packages = {
            'CentOS Linux 7.*': [
                'wget',
                'epel-release',
                'pdns',
                'pdns-backend-mysql',
                'pdns-recursor',
                'pdns-tools',
                'bind-utils',
                'httpd',
            ]
        }

        self.services = {
            'CentOS Linux 7.*': [
                'pdns',
            ]
        }

    def setup(self):
        data = self.init()
        run('hostname')
        self.install_packages()

        filer.template('/tmp/pdns.sql')
        sudo('mysql -uroot pdns -e "show tables;" | grep domain || '
             'mysql -uroot pdns < /tmp/pdns.sql')

        if env.host in data['master']['hosts']:
            data['is_master'] = True
        if env.host in data['slave']['hosts']:
            data['is_slave'] = True

        filer.template('/etc/pdns/pdns.conf', data=data)

        self.start_services().enable_services()

        if not filer.exists('/var/www/html/poweradmin'):
            sudo('cd /tmp/ && '
                 'wget http://downloads.sourceforge.net/project/poweradmin/poweradmin-2.1.7.tgz && '
                 'tar xf poweradmin-2.1.7.tgz && '
                 'mv poweradmin-2.1.7 /var/www/html/poweradmin && '
                 'chown -R apache:apache /var/www/html/poweradmin')
