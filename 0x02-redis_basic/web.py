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
    def invoker(url: str) -> str:
        """ Invoker """
        count_key = f'count:{url}'
        result_key = f'result:{url}'

        redis_store.incr(count_key)

        result = redis_store.get(result_key)
        if result:
            return result.decode('utf-8')

        result = method(url)

        redis_store.setex(result_key, 10, result)

        return result

    return invoker


@data_cacher
def get_page(url: str) -> str:
    """ Get Page """
    return requests.get(url).text


if __name__ == "__main__":
    slow_url = (
        "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
    )

    for _ in range(5):
        content = get_page(slow_url)
        print(content)

    access_count = redis_store.get(f'count:{slow_url}')
    print(f'Total Access Count for {slow_url}: {access_count.decode("utf-8")} times')
