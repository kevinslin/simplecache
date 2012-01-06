"""Memoization Functions for after program terminates
memoize
    Decorate to memoize a function during execution of the program

Methods:
========
cache(func, *args)
    Put expensive calculations into permanent cache
"""

import functools
import os
import pickle

from simplelog import log

__all__ = ["memoized", "cache"]
__version__ = '0.1.0'

SIMPLECACHE_DIR = os.path.join(os.getcwd(), '.cache')
#TODO.bug: this isn't being set by cache function
CACHE_HIT = False

def _initialize():
    """ Make sure directory exists """
    if os.path.exists(SIMPLECACHE_DIR):
        pass
    else:
        os.mkdir(SIMPLECACHE_DIR)

_initialize()
#TODO: reset if user changes this value

class memoized(object):
    """
    Decorator that caches function's return value when it is called.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:

            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:

            #TEMP: don't handle lists as args
            return self.func(*args)

    def __repr__(self):
        return self.func.__doc__

    def __get__(self, obj, objtype):
        return functools.partial(self.__call__, obj)

def cache(func, *args):
    """
    Put expensive calculatinos in cache on file that can be retrieved even after
    program has terminated
    @param:
            obj - object to be cached
    value - name of object
    @return:
            return value
    args - optional arguments given to the object
    # >>> a = binary_search(1, 12, 1)
    # >>> cache_put(a, [1, 12, 1])
    >>> cache(binary_search, 1, 12, 1) #doctest: +NORMALIZE_WHITESPACE
    3
    >>> cache(binary_search, 2, 12, 1) #doctest: +SKIP
    3
    """
    global CACHE_HIT
    _initialize()
    # Hash is function name + values
    cache_index = hash(str(func.func_name) +
            str(list(args)))
    cache_name = os.path.join( SIMPLECACHE_DIR,  str(cache_index) )

    # If we find file, load it
    if (os.path.exists(cache_name)):
        log('cache hit')
        with open(cache_name, "rb") as fh:
            r = pickle.load(fh)
            CACHE_HIT = True
            return r
    # Object doesn't exist, put it in cache
    else:
        r = func(*args)
        with open(cache_name, "wb") as fh:
            log('cache miss')
            pickle.dump(r, fh, pickle.HIGHEST_PROTOCOL)
        CACHE_HIT = False
        return r

def clear_cache():
    """
    Get rid of all itmes in the cache
    @param:
            #TODO: keep - list of items to keep
    """
    files = os.listdir(SIMPLECACHE_DIR)
    for f in files:
        os.remove(SIMPLECACHE_DIR + f)

def cache_put(obj, key):
    """
    Put an object into the cache
    @param:
    obj - a python object
    key - key to retrieve object
    @return:
    name of key
    """
    cache_index = key
    with open(SIMPLECACHE_DIR + str(cache_index), "w") as fh:
        pickle.dump(obj, fh, pickle.HIGHEST_PROTOCOL)
    return cache_index


def cache_get(key):
    """
    Get object from cache
    @param:
            key - the key to fetch object by
    """
    cache_index = hash(str(key))
    if (os.path.exists(SIMPLECACHE_DIR + str(cache_index))):
        with open(SIMPLECACHE_DIR + str(cache_index)) as fh:
            return pickle.load(fh)
    else:
        return False

