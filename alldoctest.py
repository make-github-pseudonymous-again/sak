#!/usr/bin/env python3

import os
import sys
import doctest
import functools


def doctestrecurse(*sources):

    failurecount, testcount = 0, 0

    for source in sources:

        if os.path.isfile(source):

            if source[-3:] == ".py" or source == "$":

                print(source)

                fc, tc = doctest.testfile(source)

                failurecount += fc
                testcount += tc

        elif os.path.isdir(source):

            children = os.listdir(source)
            children = map(functools.partial(os.path.join, source), children)

            fc, tc = doctestrecurse(*children)

            failurecount += fc
            testcount += tc

    return failurecount, testcount


failurecount, testcount = doctestrecurse("lib", "sak")

sys.exit(failurecount)
