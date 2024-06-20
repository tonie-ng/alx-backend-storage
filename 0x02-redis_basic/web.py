#!/usr/bin/env python3
"""request caching and tracking."""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
"""The module-level Redis instance."""


def data_cacher(method: Callable) -> Callable:
    """Data cacher"""
    @wraps(method)
    def invoker(url) -> str:
        """Cache the outout"""
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    uses the requests module to obtain the HTML content
    of a particular URL and returns it.
    """
    return requests.get(url).text
