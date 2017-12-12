# coding: utf8

"""
    Usage for check usability of proxies, remove unavailable items, and expand if not enough.
"""

import gevent

from . import (
    conn, const, spider, util
)


def patch_greenlet(func):
    """
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        return gevent.spawn(func, *args, **kwargs)

    return wrapper


def timer(after, repeat):
    """
    :param after:
    :param repeat:
    :return:
    """
    return gevent.get_hub().loop.timer(after, repeat)


class Task(object):
    CRON = {
        'update_proxies': (0, 60),
        'verify_proxies': (15, 15)
    }

    @staticmethod
    @patch_greenlet
    def do_update_proxies():
        """
        :return:
        """
        proxies = conn.RedisConnection().smembers(const.REDIS_KEY)
        if len(proxies) < const.PROXY_CRITICAL_NUM:
            s = spider.Spider()
            s.publish()

    @staticmethod
    @patch_greenlet
    def do_verify_proxies():
        """
        :return:
        """
        proxies = conn.RedisConnection().smembers(const.REDIS_KEY)
        if not proxies:
            return
        headers = {
            'user-agent': const.USER_AGENT,
            'referer': const.REFER_URL
        }
        unused = list()
        for proxy in proxies:
            p = {'proxies': 'http://{0}'.format(proxy)}
            resp = util.request_html(const.VERIFY_URL, headers=headers, proxies=p)
            if not resp:
                unused.append(proxy)
        if unused:
            conn.RedisConnection().srem(const.REDIS_KEY, *unused)


def start():
    """
    :return:
    """
    print('cron start')
    for f, t in Task.CRON.iteritems():
        print('task {0} is loading.'.format(f))
        func = getattr(Task, 'do_{0}'.format(f))
        timer(t[0] * 60, t[1] * 60).start(func)
