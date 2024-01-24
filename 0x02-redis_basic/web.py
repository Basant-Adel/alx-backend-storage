#!/usr/bin/env python3
""" Web Cache & Redis """
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """ Data Cacher """
    @wraps(method)
    def invoker(url) -> str:
        """ Invoker """
        count_key = f'count:{url}'
        result_key = f'result:{url}'

        redis_store.incr(count_key)
        result = redis_store.get(result_key)

        if result:
            return result.decode('utf-8')

        result = method(url)

        # Increment the count value
        redis_store.incr(count_key)

        # Set the result with expiration time
        redis_store.setex(result_key, 10, result)

        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """ Get Page """
    return requests.get(url).text
