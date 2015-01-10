
import lib.shieldsio, lib.markdown

iwl = lib.markdown.imagewithlink
sio = lib.shieldsio


DEFAULT = sio.DEFAULT
FLAT = sio.FLAT
FLATSQUARED = sio.FLATSQUARED

JPG = sio.JPG
PNG = sio.PNG
SVG = sio.SVG


def npmlicense ( username = None, repo = None, packagename = None, style = FLAT, fmt = SVG ) :

	title = "NPM license"
	img = sio.npmlicense( packagename, style = style, fmt = fmt )
	href = "https://raw.githubusercontent.com/%s/%s/master/LICENSE" % ( username, repo )

	return iwl( title, img, href )


def npmversion ( username = None, repo = None, packagename = None, style = FLAT, fmt = SVG ) :

	title = "NPM version"
	img = sio.npmversion( packagename, style = style, fmt = fmt )
	href = "https://www.npmjs.org/package/%s" % ( packagename )

	return iwl( title, img, href )


def npmdownloads ( username = None, repo = None, packagename = None, style = FLAT, fmt = SVG ) :

	title = "NPM downloads per month"
	img = sio.npmdownloadsmonth( packagename, style = style, fmt = fmt )
	href = "https://www.npmjs.org/package/%s" % ( packagename )

	return iwl( title, img, href )


def bowerversion ( username = None, repo = None, packagename = None, style = FLAT, fmt = SVG ) :

	title = "Bower version"
	img = sio.bowerversion( packagename, style = style, fmt = fmt )
	href = "http://bower.io/search/?q=%s" % ( packagename )

	return iwl( title, img, href )


def traviscibuild ( username = None, repo = None, packagename = None, style = FLAT, fmt = SVG ) :

	title = "Build Status"
	img = sio.travis( username, repo, style = style, fmt = fmt )
	href = "https://travis-ci.org/%s/%s" % ( username, repo )

	return iwl( title, img, href )


def droneiobuild ( username = None, repo = None, packagename = None, style = FLAT, fmt = SVG ) :

	title = "Build Status"
	img = "https://drone.io/github.com/%s/%s/status.png" % ( username, repo )
	href = "https://drone.io/github.com/%s/%s/latest" % ( username, repo )

	return iwl( title, img, href )


def coverallscoverage ( username = None, repo = None, packagename = None, style = FLAT, fmt = SVG ) :

	title = "Coverage Status"
	img = sio.coveralls( username, repo, style = style, fmt = fmt )
	href = "https://coveralls.io/r/%s/%s" % ( username, repo )

	return iwl( title, img, href )


def daviddependencies ( username = None, repo = None, packagename = None, style = FLAT, fmt = SVG ) :

	title = "Dependencies Status"
	img = sio.david( username, repo, style = style, fmt = fmt )
	href = "https://david-dm.org/%s/%s#info=dependencies" % ( username, repo )

	return iwl( title, img, href )


def daviddevdependencies ( username = None, repo = None, packagename = None, style = FLAT, fmt = SVG ) :

	title = "devDependencies Status"
	img = sio.daviddev( username, repo, style = style, fmt = fmt )
	href = "https://david-dm.org/%s/%s#info=devDependencies" % ( username, repo )

	return iwl( title, img, href )


def codeclimategpa ( username = None, repo = None, packagename = None, style = FLAT, fmt = SVG ) :

	title = "Code Climate"
	img = sio.codeclimategithub( username, repo, style = style, fmt = fmt )
	href = "https://codeclimate.com/github/%s/%s" % ( username, repo )

	return iwl( title, img, href )


def githubissues ( username = None, repo = None, packagename = None, style = FLAT, fmt = SVG ) :

	title = "GitHub issues"
	img = sio.githubissues( username, repo, style = style, fmt = fmt )
	href = "https://github.com/%s/%s/issues" % ( username, repo )

	return iwl( title, img, href )
