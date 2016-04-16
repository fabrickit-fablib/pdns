# coding: utf-8

from fabkit import run, filer, sudo
from fablib.base import SimpleBase


class PDNS(SimpleBase):
    def __init__(self):
        self.data_key = 'pdns'
        self.data = {}
        self.packages = {
            'CentOS Linux 7.*': [
                'epel-release',
                'pdns',
                'pdns-backend-mysql',
                'pdns-recursor',
                'pdns-tools',
                'bind-utils',
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

        filer.template('/etc/pdns/pdns.conf', data=data)

        self.start_services().enable_services()
