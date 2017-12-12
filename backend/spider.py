# coding: utf8

"""
    Web spiders, for crawling free ip proxies.
"""

from bs4 import BeautifulSoup

from . import (
    conn, const, util
)


class Spider(object):
    url = 'http://www.xicidaili.com/wt'

    def __init__(self, page_num=5):
        """
        :param page_num:
        """
        self.page_num = page_num

    @property
    def proxies(self):
        """
        :return:
        """
        headers = {
            'user-agent': const.USER_AGENT,
            'referer': const.REFER_URL
        }
        urls = ['{url}/{page}'.format(url=self.url, page=i + 1) for i in xrange(self.page_num)]
        for url in urls:
            html = util.request_html(url, headers=headers)
            if not html:
                print('fetch html of url {0} failed.'.format(url))
                continue
            soup = BeautifulSoup(html, 'html.parser')
            tr = soup.find('table', {'id': 'ip_list'}).find_all('tr')[1:]
            for proxy in tr:
                td = proxy.find_all('td')
                ip = td[1].get_text()
                port = td[2].get_text()
                yield ':'.join([ip, port])

    def publish(self):
        """
        :return:
        """
        proxies = [proxy for proxy in self.proxies]
        conn.RedisConnection().sadd(const.REDIS_KEY, *proxies)
