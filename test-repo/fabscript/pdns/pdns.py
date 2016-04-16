# coding: utf-8

from fabkit import task
from fablib.pdns import PDNS


@task
def setup():
    pdns = PDNS()
    pdns.setup()

    return {'status': 1}
