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
		ghb.githubissues,
		ghb.inchci
	]

	for vendor in vendors :
		cb( vendor( style = style, fmt = fmt, **fmtargs ) )

def installationinstructions ( username , name ) :

	"""

		>>> import lib.codebricks
		>>> print( lib.codebricks.installationinstructions( "abcd" , "ef-gh" ) )
		Can be managed through [jspm](https://github.com/jspm/jspm-cli),
		[duo](https://github.com/duojs/duo),
		[component](https://github.com/componentjs/component),
		[bower](https://github.com/bower/bower),
		[ender](https://github.com/ender-js/Ender),
		[jam](https://github.com/caolan/jam),
		[spm](https://github.com/spmjs/spm),
		and [npm](https://github.com/npm/npm).
		<BLANKLINE>
		## Install
		<BLANKLINE>
		### jspm
		```terminal
		jspm install github:abcd/js-ef-gh
		# or
		jspm install npm:abcd-js-ef-gh
		```
		### duo
		No install step needed for duo!
		<BLANKLINE>
		### component
		```terminal
		component install abcd/js-ef-gh
		```
		<BLANKLINE>
		### bower
		```terminal
		bower install abcd-js-ef-gh
		```
		<BLANKLINE>
		### ender
		```terminal
		ender add abcd-js-ef-gh
		```
		<BLANKLINE>
		### jam
		```terminal
		jam install abcd-js-ef-gh
		```
		<BLANKLINE>
		### spm
		```terminal
		spm install abcd-js-ef-gh --save
		```
		<BLANKLINE>
		### npm
		```terminal
		npm install abcd-js-ef-gh --save
		```
		<BLANKLINE>
		## Require
		### jspm
		```js
		let efgh = require( "github:abcd/js-ef-gh" ) ;
		// or
		import efgh from 'abcd-js-ef-gh' ;
		```
		### duo
		```js
		let efgh = require( "abcd/js-ef-gh" ) ;
		```
		<BLANKLINE>
		### component, ender, spm, npm
		```js
		let efgh = require( "abcd-js-ef-gh" ) ;
		```
		<BLANKLINE>
		### bower
		The script tag exposes the global variable `efgh`.
		```html
		<script src="bower_components/abcd-js-ef-gh/js/dist/ef-gh.min.js"></script>
		```
		Alternatively, you can use any tool mentioned [here](http://bower.io/docs/tools/).
		<BLANKLINE>
		### jam
		```js
		require( [ "abcd-js-ef-gh" ] , function ( efgh ) { ... } ) ;
		```

	"""

	packagename = username + "-js-" + name
	shortname = name.replace( "-" , "" )
	url = username + "/js-" + name

	return r"""Can be managed through [jspm](https://github.com/jspm/jspm-cli),
[duo](https://github.com/duojs/duo),
[component](https://github.com/componentjs/component),
[bower](https://github.com/bower/bower),
[ender](https://github.com/ender-js/Ender),
[jam](https://github.com/caolan/jam),
[spm](https://github.com/spmjs/spm),
and [npm](https://github.com/npm/npm).
<BLANKLINE>
## Install
<BLANKLINE>
### jspm
```terminal
jspm install github:{1}
# or
jspm install npm:{2}
```
### duo
No install step needed for duo!
<BLANKLINE>
### component
```terminal
component install {1}
```
<BLANKLINE>
### bower
```terminal
bower install {2}
```
<BLANKLINE>
### ender
```terminal
ender add {2}
```
<BLANKLINE>
### jam
```terminal
jam install {2}
```
<BLANKLINE>
### spm
```terminal
spm install {2} --save
```
<BLANKLINE>
### npm
```terminal
npm install {2} --save
```
<BLANKLINE>
## Require
### jspm
```js
let {0} = require( "github:{1}" ) ;
// or
import {0} from '{2}' ;
```
### duo
```js
let {0} = require( "{1}" ) ;
```
<BLANKLINE>
### component, ender, spm, npm
```js
let {0} = require( "{2}" ) ;
```
<BLANKLINE>
### bower
The script tag exposes the global variable `{0}`.
```html
<script src="bower_components/{2}/js/dist/{3}.min.js"></script>
```
Alternatively, you can use any tool mentioned [here](http://bower.io/docs/tools/).
<BLANKLINE>
### jam
```js
require( [ "{2}" ] , function ( {0} ) {{ ... }} ) ;
```""".format( shortname , url , packagename , name )
