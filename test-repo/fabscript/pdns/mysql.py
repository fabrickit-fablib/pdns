# coding: utf-8

from fabkit import task
from fablib.mysql import MySQL


@task
def setup():
    mysql = MySQL()
    mysql.setup()
    return {'status': 1}
