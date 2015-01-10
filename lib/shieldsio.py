
import functools

# visit http://shields.io/ for spec

DEFAULT = "default"
FLAT = "flat"
FLATSQUARED = "flat-square"

STYLE = [ DEFAULT, FLAT, FLATSQUARED ]

JPG = "jpg"
PNG = "png"
SVG = "svg"

FORMAT = [ JPG, PNG, SVG ]


def imgurl ( path, style = FLAT, fmt = SVG ) :

	if style == DEFAULT :
		return "http://img.shields.io/%s.%s" % ( path, fmt )
	else :
		return "http://img.shields.io/%s.%s?style=%s" % ( path, fmt, style )


def escape ( string ) :

	string = string.replace( "-", "--" )
	string = string.replace( "_", "__" )
	string = string.replace( " ", "_" )

	return string


def custom ( subject, status, color, style = FLAT, fmt = SVG ) :

	subject = escape( subject )
	status = escape( status )
	color = escape( color )

	path = "badge/%s-%s-%s" % ( subject, status, color )

	return imgurl( path, style, fmt )


def service ( *args, **kwargs ) :

	style = kwargs.get( "style", FLAT )
	fmt = kwargs.get( "fmt", SVG )

	args = map( str, args )

	path = '/'.join( args )

	return imgurl( path, style, fmt )


npm = functools.partial( service, "npm" )

npmlicense = functools.partial( npm, "l" )
npmversion = functools.partial( npm, "v" )
npmdownloadsmonth = functools.partial( npm, "dm" )

bower = functools.partial( service, "bower" )
bowerversion = functools.partial( bower, "v" )

github = functools.partial( service, "github" )
githubissues = functools.partial( github, "issues" )
githubtag = functools.partial( github, "tag" )
githubrelease = functools.partial( github, "release" )

scrutinizer = functools.partial( service, "scrutinizer" )
scrutinizerquality = functools.partial( scrutinizer, "g" )
scrutinizercoverage = functools.partial( scrutinizer, "coverage/g" )

travis = functools.partial( service, "travis" )

coveralls = functools.partial( service, "coveralls" )

codeclimate = functools.partial( service, "codeclimate" )
codeclimategithub = functools.partial( codeclimate, "github" )
codeclimatecoverage = functools.partial( codeclimate, "coverage" )
codeclimatecoveragegithub = functools.partial( codeclimatecoverage, "github" )

david = functools.partial( service, "david" )
daviddev = functools.partial( david, "dev" )
davidpeer = functools.partial( david, "peer" )
