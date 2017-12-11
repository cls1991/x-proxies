# coding: utf8

"""
    Redis connection pool management.
"""

import redis


class RedisConfig(object):
    HOST = '127.0.0.1'
    PORT = 6379
    DB = 0


class RedisConnection(object):

    def __init__(self):
        if not hasattr(RedisConnection, 'pool'):
            RedisConnection.create_pool()
        self.connection_pool = redis.Redis(connection_pool=RedisConnection.pool)

    @staticmethod
    def create_pool():
        """
        :return:
        """
        RedisConnection.pool = redis.ConnectionPool(
            host=RedisConfig.HOST,
            port=RedisConfig.PORT,
            db=RedisConfig.DB
        )

    def get(self, key):
        """
        :param key:
        :return:
        """
        return self.connection_pool.get(key)

    def set(self, key, value):
        """
        :param key:
        :param value:
        :return:
        """
        return self.connection_pool.set(key, value)

    def sadd(self, key, *values):
        """
        :param key:
        :param values:
        :return:
        """
        return self.connection_pool.sadd(key, *values)

    def srem(self, key, *values):
        """
        :param key:
        :param values:
        :return:
        """
        return self.connection_pool.srem(key, *values)

    def smembers(self, key):
        """
        :param key:
        :return:
        """
        return self.connection_pool.smembers(key)
