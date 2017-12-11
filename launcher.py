# coding: utf8

"""
    launcher.py: start web crawler service, flask api service.
"""

import os

from backend import spider

# checkout to project directory
project = os.path.split(os.path.realpath(__file__))[0]
os.chdir(project)


def main():
    """
    :return:
    """
    s = spider.Spider()
    for proxy in s.proxies:
        print(proxy)


if __name__ == '__main__':
    main()
