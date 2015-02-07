import lib.sys , lib.args

@lib.args.convert( start = int , end = int )
def cut ( source, dest, start, end ) :
	lib.sys.call([
		"pdftk",
		"A=%s" % source,
		"cat",
		"A%d-%d" % (start, end),
		"output",
		dest
	], stddefault = None)


def burst ( source, *others ) :

	lib.sys.call( [
		"pdftk",
		source,
		"burst"
	], stddefault = None )

	if others : burst( *others )


def svg ( source, *others ) :

	lib.sys.call( [
		"pdftocairo",
		"-svg",
		source
	], stddefault = None )

	if others : svg( *others )
