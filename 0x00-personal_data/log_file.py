#!/usr/bin/env python3
import logging
from functools import wraps, lru_cache


memoize_dict = {}


def decorator(max_size=10):
    def inner_func(original_func):

        @wraps(original_func)
        def wrapper(n):
            print("memoize_dict", memoize_dict)
            if n in memoize_dict:
                print("hit")
                return memoize_dict[n]
            value = original_func(n)
            if len(memoize_dict) >= max_size and value not in memoize_dict:
                memoize_dict.popitem()
            memoize_dict[value] = value
            return value
        return wrapper
    return inner_func


@lru_cache(maxsize=1000)
def fib(n: int):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)


print(fib(500))
