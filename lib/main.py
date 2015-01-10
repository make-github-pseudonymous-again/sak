
import functools, lib.args, lib.error

accepts = functools.partial( lib.args.accepts, lib.error.OptionOfWrongTypeException )
