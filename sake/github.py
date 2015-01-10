import lib.config, lib.git, lib.error, lib.check, lib.curl
import lib.github, lib.input, lib.http, lib.args
import re

DOMAIN = lib.github.DOMAIN
CONFIG_KEY = lib.github.CONFIG_KEY
LICENSES = lib.github.LICENSES
GITIGNORES = lib.github.GITIGNORES
TRUE = lib.github.TRUE
FALSE = lib.github.FALSE
BOOLEANS = lib.github.BOOLEANS
YOU = lib.github.YOU
NEWEST = lib.github.NEWEST
OLDEST = lib.github.OLDEST
STARGAZERS = lib.github.STARGAZERS
SORT = lib.github.SORT



def clone( repo, dest = None, username = None ):

	url = lib.http.url( DOMAIN, repo, username, secure = True )

	if dest is not None :
		return lib.git.clone( url, dest )
	else :
		return lib.git.clone( url )


def new(name, org = None, team_id = None, username = None, password = None, auto_init = FALSE, private = FALSE, description = None, homepage = None, has_issues = TRUE, has_wiki = TRUE, has_downloads = TRUE, gitignore_template = None, license_template = None):

	lib.check.OptionNotInListException( "private", private, BOOLEANS )
	lib.check.OptionNotInListException( "has_issues", has_issues, BOOLEANS )
	lib.check.OptionNotInListException( "has_wiki", has_wiki, BOOLEANS )
	lib.check.OptionNotInListException( "has_downloads", has_downloads, BOOLEANS )
	lib.check.OptionNotInListException( "auto_init", auto_init, BOOLEANS )
	lib.check.OptionNotInListException( "gitignore_template", gitignore_template, GITIGNORES )
	lib.check.OptionNotInListException( "license_template", license_template, LICENSES )

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
		url = lib.github.api( "user" , "repos" )
	else :
		url = lib.github.api( "orgs" , org , "repos" )

	_, _, p = lib.curl.postjson(url, parameters, username, password, stddefault = None)
	print()
	lib.check.SubprocessReturnedFalsyValueException(p.args, p.returncode)


def group ( *names ) :

	username, password = lib.github.credentials( None, None )

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


	for name in names :
		new(name, org, team_id, username, password, auto_init, private, description, homepage, has_issues, has_wiki, has_downloads, gitignore_template, license_template)


def list(target = YOU, name = None, t = None, username = None, password = None):
	for repo in lib.github.list(target, name, t, username, password):
		print(repo["full_name"])


def download ( target = YOU, name = None, t = None, username = None, password = None, prompt = True, prefix = "", suffix = "", regexp = "" ) :

	for repo in lib.github.list( target, name, t, username, password):

		repo = repo["full_name"]

		take = True

		take = take and ( not prefix or repo.startswith( prefix ) )
		take = take and ( not suffix or repo.endswith( suffix ) )
		take = take and ( not regexp or re.match( regexp, repo ) is not None )

		if take and ( not prompt or lib.input.yesorno( "clone '%s'?" % repo ) ) :
			clone( repo, username = username )


def delete(owner, repo, username = None, password = None):
	username, password = lib.github.credentials(username, password)

	url = lib.github.api( "repos" , owner , repo )
	_, _, p = lib.curl.deletejson(url, username = username, password = password, stddefault = None)
	print()
	lib.check.SubprocessReturnedFalsyValueException(p.args, p.returncode)



def issues( owner = None , repo = None , user = False, org = None, username = None, password = None, filter = None, state = None, labels = None, sort = None, direction = None, since = None ) :

	for issue in lib.args.forward( lib.github.issues , locals( ) ) :

		print( issue )



def createissue ( owner, repo, title, body = None, assignee = None, milestone = None, labels = None, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/#create-an-issue
	"""

	url = lib.github.api( "repos", owner, repo, "issues" )

	labels = lib.args.listify( labels )

	parameters = dict( title = title, body = body, assignee = assignee, milestone = milestone, labels = labels )

	username, password = lib.github.credentials(username, password)

	_, _, p = lib.curl.postjson(url, parameters, username, password, stddefault = None)
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def closeissues ( owner , repo , *issuenos , username = None , password = None ) :
	pass

def migrateissues ( owner , origin , destination , *issuenos , username = None , password = None ) :
	pass


def labels ( owner, repo, name = None, issue = None, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	if issue is not None :
		url = lib.github.api( "repos", owner, repo, "issues", issue, "labels" )
	elif name is not None :
		url = lib.github.api( "repos", owner, repo, "labels", name )
	else :
		url = lib.github.api( "repos", owner, repo, "labels" )

	_, _, p = lib.curl.getjson( url, None, username, password, stddefault = None )
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def createlabel ( owner, repo, name, color, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	url = lib.github.api( "repos", owner, repo, "labels" )

	parameters = dict( name = name, color = color )

	username, password = lib.github.credentials(username, password)

	_, _, p = lib.curl.postjson(url, parameters, username, password, stddefault = None)
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def updatelabel ( owner, repo, oldname, newname, color, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	url = lib.github.api( "repos", owner, repo, "labels", oldname )

	parameters = dict( name = newname, color = color )

	username, password = lib.github.credentials( username, password )

	_, _, p = lib.curl.patchjson( url, parameters, username, password, stddefault = None )
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )



def deletelabel ( owner, repo, name, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	url = lib.github.api( "repos", owner, repo, "labels", name )

	username, password = lib.github.credentials( username, password )

	_, _, p = lib.curl.deletejson( url, None, username, password, stddefault = None )
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def addlabels ( owner, repo, issue, labels = None, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	labels = lib.args.listify( labels )

	username, password = lib.github.credentials( username, password )

	url = lib.github.api( "repos", owner, repo, "issues", issue, "labels" )

	_, _, p = lib.curl.postjson( url, labels, username, password, stddefault = None )
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def removelabel ( owner, repo, issue, label, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	username, password = lib.github.credentials( username, password )

	url = lib.github.api( "repos", owner, repo, "issues", issue, "labels", label )

	_, _, p = lib.curl.deletejson( url, None, username, password, stddefault = None )
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def updatelabels ( owner, repo, issue, labels = None, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	labels = lib.args.listify( labels )

	username, password = lib.github.credentials( username, password )

	url = lib.github.api( "repos", owner, repo, "issues", issue, "labels" )

	_, _, p = lib.curl.putjson( url, labels, username, password, stddefault = None )
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def removealllabels ( owner, repo, issue, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	username, password = lib.github.credentials( username, password )

	url = lib.github.api( "repos", owner, repo, "issues", issue, "labels" )

	_, _, p = lib.curl.deletejson( url, None, username, password, stddefault = None )
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def milestonelabels ( owner, repo, milestone, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	url = lib.github.api( "repos", owner, repo, "milestones", milestone, "labels" )

	_, _, p = lib.curl.getjson( url, None, username, password, stddefault = None )
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def listforks ( owner, repo, sort = NEWEST, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	if username is not None :
		username, password = lib.github.credentials( username, password )

	url = lib.github.api( "repos", owner, repo, "forks" )

	parameters = dict( sort = sort )

	_, _, p = lib.curl.getjson( url, parameters, username, password, stddefault = None )
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def fork ( owner, repo, organization = None, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	username, password = lib.github.credentials( username, password )

	url = lib.github.api( "repos", owner, repo, "forks" )

	parameters = dict( organization = organization )

	_, _, p = lib.curl.postjson( url, parameters, username, password, stddefault = None )
	print()
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )


def patch ( owner, repo, name, username = None, password = None, private = FALSE, description = None, homepage = None, has_issues = TRUE, has_wiki = TRUE, has_downloads = TRUE, default_branch = None ) :

	lib.check.OptionNotInListException( "private", private, BOOLEANS )
	lib.check.OptionNotInListException( "has_issues", has_issues, BOOLEANS )
	lib.check.OptionNotInListException( "has_wiki", has_wiki, BOOLEANS )
	lib.check.OptionNotInListException( "has_downloads", has_downloads, BOOLEANS )

	username, password = lib.github.credentials(username, password)


	parameters = {
		"name" : name,
		"description" : description,
		"homepage" : homepage,
		"private": private,
		"has_issues" : has_issues,
		"has_wiki" : has_wiki,
		"has_downloads" : has_downloads,
		"default_branch": default_branch
	}


	url = lib.github.api( "repos", owner, repo )

	_, _, p = lib.curl.patchjson(url, parameters, username, password, stddefault = None)
	print()
	lib.check.SubprocessReturnedFalsyValueException(p.args, p.returncode)



def archive ( username , forks = False , gist = True , metadata = True ) :
	"""
		All credits go to Filippo Valsorda (https://filippo.io).

		original -> https://filippo.io/archive-your-github-repo-and-data/

		# This is free and unencumbered software released into the public domain.

		# Anyone is free to copy, modify, publish, use, compile, sell, or
		# distribute this software, either in source code form or as a compiled
		# binary, for any purpose, commercial or non-commercial, and by any
		# means.

		# In jurisdictions that recognize copyright laws, the author or authors
		# of this software dedicate any and all copyright interest in the
		# software to the public domain. We make this dedication for the benefit
		# of the public at large and to the detriment of our heirs and
		# successors. We intend this dedication to be an overt act of
		# relinquishment in perpetuity of all present and future rights to this
		# software under copyright law.

		# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
		# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
		# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
		# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
		# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
		# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
		# OTHER DEALINGS IN THE SOFTWARE.

		# For more information, please refer to <http://unlicense.org/>

		usage: gh_dump.py [-h] [--forks] [--no-gist] [--no-metadata] username

		Dump an user's public GitHub data into current directory.

		positional arguments:
		username the GH username

		optional arguments:
		-h, --help show this help message and exit
		--forks git clone also forks (default is don't)
		--no-gist don't download user gists (default is do)
		--no-metadata don't download user metadata (default is do)
	"""

	from urllib.request import urlopen
	from subprocess import call
	import json
	import re
	import os.path

	def clear_url(url):
		return re.sub(r'\{[^\}]*\}', '', url)

	data = urlopen('https://api.github.com/users/' + args.user).read()
	user = json.loads(data.decode('utf-8'))
	if args.metadata:
		with open('user.json', 'wb') as f:
			f.write(data)

	data = urlopen(clear_url(user['repos_url'])).read()
	repos = json.loads(data.decode('utf-8'))
	if args.metadata:
		with open('repos.json', 'wb') as f:
			f.write(data)
	for repo in repos:
		if not repo['fork']:
			call(['git', 'clone', repo['clone_url']])
		elif args.forks:
			if not os.path.exists('forks'):
				os.makedirs('forks')
			call(['git', 'clone', repo['clone_url'], os.path.join('forks', repo['name'])])

	data = urlopen(clear_url(user['gists_url'])).read()
	gists = json.loads(data.decode('utf-8'))
	if args.metadata:
		with open('gists.json', 'wb') as f:
			f.write(data)
	if args.gists:
		if not os.path.exists('gists'):
			os.makedirs('gists')
		for gist in gists:
			call(['git', 'clone', gist['git_pull_url'], os.path.join('gists', gist['id'])])

	if args.metadata:
		for name in ['received_events', 'events', 'organizations', 'followers', 'starred', 'following', 'subscriptions']:
			data = urlopen(clear_url(user[name + '_url'])).read()
			with open(name + '.json', 'wb') as f:
				f.write(data)
