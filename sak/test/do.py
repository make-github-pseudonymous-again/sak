"""
	Doc for sak.test.do
"""

import time
import itertools
import lib.fn
import lib.args


def action(a, b=10):
    """
            Doc for sak.test.do.action
    """
    print(a, b)


@lib.args.convert(times=int, interval=int)
def throttled(times, interval):

    @lib.fn.throttle(times, interval)
    def fn(i):
        print(i, time.time())

    for i in itertools.count(1):
        fn(i)
