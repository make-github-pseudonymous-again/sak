from __future__ import absolute_import, division, print_function, unicode_literals

TRAVISCI = "travis-ci"
DRONEIO = "drone.io"

CI = [TRAVISCI, DRONEIO]

def qualifiedname ( username, repo ) :
	return "%s-%s" % (username, repo)


def formatargs ( username, repo ) :

	return dict(
		username = username,
		repo = repo,
		qualifiedname = qualifiedname(username, repo)
	)

def badges ( username, repo, ci, cb ) :

	fmtargs = formatargs(username, repo)

	cb( "[![NPM license](http://img.shields.io/npm/l/%(qualifiedname)s.svg)](https://raw.githubusercontent.com/%(username)s/%(repo)s/master/LICENSE)" % fmtargs)
	cb( "[![NPM version](http://img.shields.io/npm/v/%(qualifiedname)s.svg)](https://www.npmjs.org/package/%(qualifiedname)s)" % fmtargs)
	cb( "[![Bower version](http://img.shields.io/bower/v/%(qualifiedname)s.svg)](http://bower.io/search/?q=%(qualifiedname)s)" % fmtargs)
	if ci == TRAVISCI :
		cb( "[![Build Status](https://travis-ci.org/%(username)s/%(repo)s.svg)](https://travis-ci.org/%(username)s/%(repo)s)" % fmtargs)
	elif ci == DRONEIO :
		cb( "[![Build Status](https://drone.io/github.com/%(username)s/%(repo)s/status.png)](https://drone.io/github.com/%(username)s/%(repo)s/latest)" % fmtargs)
	cb( "[![Coverage Status](https://coveralls.io/repos/%(username)s/%(repo)s/badge.png)](https://coveralls.io/r/%(username)s/%(repo)s)" % fmtargs)
	cb( "[![Dependencies Status](https://david-dm.org/%(username)s/%(repo)s.png)](https://david-dm.org/%(username)s/%(repo)s#info=dependencies)" % fmtargs)
	cb( "[![devDependencies Status](https://david-dm.org/%(username)s/%(repo)s/dev-status.png)](https://david-dm.org/%(username)s/%(repo)s#info=devDependencies)" % fmtargs)
	cb( "[![Code Climate](https://codeclimate.com/github/%(username)s/%(repo)s.png)](https://codeclimate.com/github/%(username)s/%(repo)s)" % fmtargs)
	cb( "[![NPM downloads per month](http://img.shields.io/npm/dm/%(qualifiedname)s.svg)](https://www.npmjs.org/package/%(qualifiedname)s)" % fmtargs)
	cb( "[![GitHub issues](http://img.shields.io/github/issues/%(username)s/%(repo)s.svg)](https://github.com/%(username)s/%(repo)s/issues)" % fmtargs)
