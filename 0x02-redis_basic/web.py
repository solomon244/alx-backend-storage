#!/usr/bin/env python3
'''Implementing an expiring web cache and tracker
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''Redis instance.
'''


def data_cacher(func: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(func)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_store.incr(f'count:{url}')
        n = redis_store.get(f'n:{url}')
        if n:
            return n.decode('utf-8')
        n = func(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'n:{url}', 10, n)
        return n
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''track how many times a particular URL was accessed in the key "count:{url}" and cache the result with an expiration time of 10 seconds.
    '''
    return requests.get(url).text
