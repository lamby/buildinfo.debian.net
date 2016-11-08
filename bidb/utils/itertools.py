from __future__ import absolute_import

import itertools

def groupby(iterable, keyfunc, sortfunc=lambda x: x):
    return [
        (x, list(sorted(y, key=sortfunc)))
        for x, y in itertools.groupby(iterable, keyfunc)
    ]
