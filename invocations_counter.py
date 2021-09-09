import functools


def counter(fn):
    @functools.wraps(fn)
    def helper(*args, **kwargs):
        helper.invocations += 1
        return fn(*args, **kwargs)
    helper.invocations = 0
    return helper
