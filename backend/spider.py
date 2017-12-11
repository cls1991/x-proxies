# coding: utf8

"""
    Web spiders, for crawling free ip proxies.
"""

import time

import requests
from bs4 import BeautifulSoup

import const


class Spider(object):
    url = 'http://www.xicidaili.com/wt'

    def __init__(self, page_num=5):
        """
        :param page_num:
        """
        self.page_num = page_num

    def request_html(self, url):
        """
        :param url:
        :return:
        """
        headers = {
            'user-agent': const.USER_AGENT,
            'referer': const.REFER_URL
        }
        resp = None
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                resp = r.text
        except requests.RequestException as e:
            print(e)
        finally:
            time.sleep(2)

        return resp

    @property
    def proxies(self):
        """
        :return:
        """
        urls = ['{url}/{page}'.format(url=self.url, page=i + 1) for i in xrange(self.page_num)]
        for url in urls:
            html = self.request_html(url)
            if not html:
                print('fetch html of url %s failed.' % url)
                continue
            soup = BeautifulSoup(html, 'html.parser')
            tr = soup.find('table', {'id': 'ip_list'}).find_all('tr')[1:]
            for proxy in tr:
                td = proxy.find_all('td')
                ip = td[1].get_text()
                port = td[2].get_text()
                yield ':'.join([ip, port])
