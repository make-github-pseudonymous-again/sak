
import functools
import lib.args
import lib.error

accepts = functools.partial(
    lib.args.accepts, lib.error.OptionOfWrongTypeException)
