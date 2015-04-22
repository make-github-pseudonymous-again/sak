import lib.ghbadges as ghb

TRAVISCI = "travis-ci"
DRONEIO = "drone.io"

CI = [TRAVISCI, DRONEIO]

def qualifiedname ( username, repo ) :
	return "%s-%s" % ( username, repo )


def formatargs ( username, repo ) :

	return dict(
		username = username,
		repo = repo,
		packagename = qualifiedname( username, repo )
	)


DEFAULT = ghb.DEFAULT
FLAT = ghb.FLAT
FLATSQUARED = ghb.FLATSQUARED

JPG = ghb.JPG
PNG = ghb.PNG
SVG = ghb.SVG


def badges ( username, repo, ci, cb, style = FLAT, fmt = SVG ) :

	fmtargs = formatargs( username, repo )

	vendors = [
		ghb.npmlicense,
		ghb.npmversion,
		ghb.bowerversion,
		ghb.traviscibuild if ci == TRAVISCI else ghb.droneiobuild,
		ghb.coverallscoverage,
		ghb.daviddependencies,
		ghb.daviddevdependencies,
		ghb.codeclimategpa,
		ghb.npmdownloads,
		ghb.githubissues
	]

	for vendor in vendors :
		cb( vendor( style = style, fmt = fmt, **fmtargs ) )

def installationinstructions ( username , name ) :

	"""

		>>> import lib.codebricks
		>>> print( lib.codebricks.installationinstructions( "abcd" , "efgh" ) )
		Can be managed through [duo](https://github.com/duojs/duo),
		[component](https://github.com/componentjs/component),
		[bower](https://github.com/bower/bower), or
		[npm](https://github.com/npm/npm).
		<BLANKLINE>
		```js
		let efgh = require( "abcd-js-efgh" ) ;
		```

	"""

	return r"""Can be managed through [duo](https://github.com/duojs/duo),
[component](https://github.com/componentjs/component),
[bower](https://github.com/bower/bower), or
[npm](https://github.com/npm/npm).

```js
let {1} = require( "{0}-js-{1}" ) ;
```""".format( username , name )
