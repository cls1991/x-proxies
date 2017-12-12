# coding: utf8

"""
    Support get, refresh requests.
"""

from flask import (
    Flask, jsonify, make_response
)

from backend import (
    conn, const
)

app = Flask(__name__)


@app.route('/proxies')
def get_proxies():
    """
    :return:
    """
    proxies = conn.RedisConnection().smembers(const.REDIS_KEY)
    return jsonify({'proxies': list(proxies)})


@app.errorhandler(404)
def not_found(error):
    """
    :return:
    """
    return make_response(jsonify({'error': 'Not found'}), 404)
