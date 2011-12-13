import functools
import os
import pickle
from simplelog import SL as sl

sl.quiet()

"""
A really simple cache
"""
class memoized(object):
    """
    Decorator that caches function's return value when it is called.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            sl.debug("fetching from cache...")
            return self.cache[args]
        except KeyError:
            sl.debug("cache miss...")
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            sl.debug("uncachable...")
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
    sl.debug("========\nin cache")
    sl.debug("obj: %s" % str(func))
    cache_index = hash(str(func.func_name) + str(list(args))) #hash is function name + values
    if not (os.path.exists(".cache")):
        os.mkdir(".cache")
    sl.debug("index: %s" % str(cache_index))
    #Check if file is in cache
    if (os.path.exists(".cache/"+str(cache_index))):
        sl.debug("found item in cache")
        with open(".cache/"+str(cache_index), "rb") as fh:
            r = pickle.load(fh)
            #sl.debug("item: %s" % str(r))
            return r
    else:
        sl.debug("putting item in cache")
        r = func(*args)
        sl.debug("function result: %s" % str(r))
        with open(".cache/"+str(cache_index), "wb") as fh:
            pickle.dump(r, fh, pickle.HIGHEST_PROTOCOL)
        return r

def clear_cache():
    """
    Get rid of all itmes in the cache
    @param:
            #TODO: keep - list of items to keep
    """
    files = os.listdir(".cache")
    for f in files:
        os.remove(".cache/" + f)

def cache_put(obj, key):
    """
    Put an object into the cache
    @param:
    obj - a python object
    key - key to retrieve object
    @return:
    name of key
    """
    #TODO: catch error
    cache_index = key
    with open(".cache/"+str(cache_index), "w") as fh:
        pickle.dump(obj, fh, pickle.HIGHEST_PROTOCOL)
    return cache_index


def cache_get(key):
    """
    Get object from cache
    @param:
            key - the key to fetch object by
    """
    cache_index = hash(str(key))
    if (os.path.exists(".cache/"+str(cache_index))):
        with open(".cache/"+str(cache_index)) as fh:
            return pickle.load(fh)
    else:
        return False

