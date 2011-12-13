import simplecache

@simplecache.memoized
def fib(n):
    """ Return nth fib number"""
    # 0, 1, 1, 2 ...
    if n in (0, 1):
        return n
    return fib(n-1) + fib(n-2)

print("Bond here")
