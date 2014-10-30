from __future__ import absolute_import, division, print_function, unicode_literals

import lib.config, lib.git, lib.error, lib.check, lib.curl, lib.github, lib.input, lib.http

DOMAIN = lib.github.DOMAIN
CONFIG_KEY = lib.github.CONFIG_KEY
LICENSES = lib.github.LICENSES
GITIGNORES = lib.github.GITIGNORES
TRUE = lib.github.TRUE
FALSE = lib.github.FALSE
BOOLEANS = lib.github.BOOLEANS
YOU = lib.github.YOU


def apiurl ( *args ) :

	args = map( str, args )

	return "https://api.github.com/" + '/'.join( args )


def clone(repo, username = None):

	url = lib.http.url(DOMAIN, repo, username, secure = True)
	return lib.git.clone(url)


def new(name, org = None, team_id = None, username = None, password = None, auto_init = FALSE, private = FALSE, description = None, homepage = None, has_issues = TRUE, has_wiki = TRUE, has_downloads = TRUE, gitignore_template = None, license_template = None):

	lib.check.OptionNotInListException("private", private, BOOLEANS)
	lib.check.OptionNotInListException("has_issues", has_issues, BOOLEANS)
	lib.check.OptionNotInListException("has_wiki", has_wiki, BOOLEANS)
	lib.check.OptionNotInListException("has_downloads", has_downloads, BOOLEANS)
	lib.check.OptionNotInListException("auto_init", auto_init, BOOLEANS)
	lib.check.OptionNotInListException("gitignore_template", gitignore_template, GITIGNORES)
	lib.check.OptionNotInListException("license_template", license_template, LICENSES)

	username, password = lib.github.credentials(username, password)


	parameters = {
		"name" : name,
		"description" : description,
		"homepage" : homepage,
		"private": private,
		"has_issues" : has_issues,
		"has_wiki" : has_wiki,
		"has_downloads" : has_downloads,
		"team_id": team_id,
		"auto_init" : auto_init,
		"gitignore_template" : gitignore_template,
		"license_template" : license_template
	}


	if org is None :
		url = "https://api.github.com/user/repos"
	else :
		url = "https://api.github.com/orgs/%s/repos" % org

	_, _, p = lib.curl.postjson(url, parameters, username, password, stddefault = None)
	print()
	lib.check.SubprocessReturnedFalsyValueException(p.args, p.returncode)


def group(*names):

	username, password = lib.github.credentials(None, None)

	org = None
	team_id = None
	auto_init = FALSE
	private = FALSE
	description = None
	homepage = None
	has_issues = TRUE
	has_wiki = TRUE
	has_downloads = TRUE
	gitignore_template = None
	license_template = None


	for name in names:
		new(name, org, team_id, username, password, auto_init, private, description, homepage, has_issues, has_wiki, has_downloads, gitignore_template, license_template)


def list(target = YOU, name = None, t = None, username = None, password = None):
	for repo in lib.github.list(target, name, t, username, password):
		print(repo["full_name"])


def download(target = YOU, name = None, t = None, username = None, password = None, prompt = True):
	for repo in lib.github.list(target, name, t, username, password):
		repo = repo["full_name"]
		if not prompt or lib.input.yesorno("clone '%s'?" % repo) :
			clone(repo, username)


def delete(owner, repo, username = None, password = None):
	username, password = lib.github.credentials(username, password)

	url = "https://api.github.com/repos/%s/%s" % (owner, repo)
	_, _, p = lib.curl.deletejson(url, username = username, password = password, stddefault = None)
	print()
	lib.check.SubprocessReturnedFalsyValueException(p.args, p.returncode)



def issues( user = False, org = None, username = None, password = None, filter = None, state = None, labels = None, sort = None, direction = None, since = None ) :

	"""
		https://developer.github.com/v3/issues/
	"""

	username, password = lib.github.credentials(username, password)

	if user :
		url = "https://api.github.com/user/issues"
	elif org is None :
		url = "https://api.github.com/orgs/%s/issues" % org
	else :
		url = "https://api.github.com/issues"

	parameters = {
		"filter" : filter,
		"state" : state,
		"labels" : labels,
		"sort": sort,
		"direction" : direction,
		"since" : since
	}

	_, _, p = lib.curl.getjson(url, parameters, username, password, stddefault = None)
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def labels ( owner, repo, name = None, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	if name is None :
		url = apiurl( "repos", owner, repo, "labels" )
	else :
		url = apiurl( "repos", owner, repo, "labels", name )

	_, _, p = lib.curl.getjson(url, None, username, password, stddefault = None)
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def createlabel ( owner, repo, name, color, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	url = apiurl( "repos", owner, repo, "labels" )

	parameters = dict( name = name, color = color )

	username, password = lib.github.credentials(username, password)

	_, _, p = lib.curl.postjson(url, parameters, username, password, stddefault = None)
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def updatelabel ( owner, repo, oldname, newname, color, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	url = apiurl( "repos", owner, repo, "labels", oldname )

	parameters = dict( name = newname, color = color )

	username, password = lib.github.credentials(username, password)

	_, _, p = lib.curl.patchjson(url, parameters, username, password, stddefault = None)
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )



def deletelabel ( owner, repo, name, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	url = apiurl( "repos", owner, repo, "labels", name )

	username, password = lib.github.credentials( username, password )

	_, _, p = lib.curl.deletejson( url, None, username, password, stddefault = None )
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )
