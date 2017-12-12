# coding: utf8

"""
    Usage for check usability of proxies, remove unavailable items, and expand if not enough.
"""

import gevent


def patch_greenlet(func):
    """
    :param func:
    :return:
    """

    def inner(*args, **kwargs):
        return gevent.spawn(func, *args, **kwargs)

    return inner


class Scheduler(object):

    @patch_greenlet
    def check_proxies(self):
        """
        :return:
        """
        print('check_proxies')


def start():
    """
    :return:
    """
    loop = gevent.get_hub().loop
    t = loop.timer(0, 15)
    f = Scheduler().check_proxies
    t.start(f)
