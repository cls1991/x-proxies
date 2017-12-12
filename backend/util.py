# coding: utf8

"""
    Common tool functions.
"""

import requests

import const


def request_html(url, method='GET', headers=None, proxies=None):
    """
    :param url:
    :param method:
    :param headers:
    :param proxies:
    :return:
    """
    resp = None
    try:
        r = requests.request(method, url, headers=headers, proxies=proxies)
        if r.status_code == 200:
            resp = r.text
    except requests.RequestException as e:
        print(e)

    return resp
