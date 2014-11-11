# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import functools, lib.args, lib.error

accepts = functools.partial( lib.args.accepts, lib.error.OptionOfWrongTypeException )
