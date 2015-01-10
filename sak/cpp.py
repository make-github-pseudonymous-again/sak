import lib.cpplint, lib.args


def lint(*args, **kwargs):

	items = kwargs.items()

	options = [lib.args.format(key, val) for key, val in items]

	options.extend(args)

	lib.cpplint.main(*options)
