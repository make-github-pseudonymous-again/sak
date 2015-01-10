import lib.config, lib.git, lib.hg, lib.error, lib.check, json, lib.sys, lib.bitbucket, lib.input, lib.bytes

DOMAIN = lib.bitbucket.DOMAIN
CONFIG_KEY = lib.bitbucket.CONFIG_KEY
ALLOW_FORKS = lib.bitbucket.ALLOW_FORKS
NO_PUBLIC_FORKS = lib.bitbucket.NO_PUBLIC_FORKS
NO_FORKS = lib.bitbucket.NO_FORKS
FORK_POLICIES = lib.bitbucket.FORK_POLICIES
GIT = lib.bitbucket.GIT
HG = lib.bitbucket.HG
SCMS = lib.bitbucket.SCMS
TRUE = lib.bitbucket.TRUE
FALSE = lib.bitbucket.FALSE
BOOLEANS = lib.bitbucket.BOOLEANS
LANGUAGES = lib.bitbucket.LANGUAGES
USER = lib.bitbucket.USER
TEAM = lib.bitbucket.TEAM


def clone(repo, username = None, scm = GIT):

	url = lib.http.url(DOMAIN, repo, username, secure = True)
	if scm == GIT : lib.git.clone(url)
	else : lib.hg.clone(url)


def new(repository, owner = None, username = None, password = None, is_private = TRUE, scm = GIT, fork_policy = NO_PUBLIC_FORKS, name = None, description = None, language = None, has_issues = FALSE, has_wiki = FALSE):

	lib.check.OptionNotInListException("scm", scm, SCMS)
	lib.check.OptionNotInListException("language", language, LANGUAGES)
	lib.check.OptionNotInListException("has_wiki", has_wiki, BOOLEANS)
	lib.check.OptionNotInListException("has_issues", has_issues, BOOLEANS)
	lib.check.OptionNotInListException("is_private", is_private, BOOLEANS)
	lib.check.OptionNotInListException("fork_policy", fork_policy, FORK_POLICIES)

	username, password = lib.config.prompt_cred(DOMAIN, CONFIG_KEY, username, password)

	if owner is None : owner = username

	parameters = {
		"scm": scm,
		"is_private": is_private,
		"fork_policy": fork_policy,
		"name" : name,
		"description" : description,
		"language" : language,
		"has_issues" : has_issues,
		"has_wiki" : has_wiki
	}

	url = "https://api.bitbucket.org/2.0/repositories/%s/%s" % (owner, repository)

	_, _, p = lib.curl.postjson(url, parameters, username, password, stddefault = None)
	print()
	lib.check.SubprocessReturnedFalsyValueException(p.args, p.returncode)


def group(owner, language, *repositories):

	username, password = lib.config.prompt_cred(DOMAIN, CONFIG_KEY, None, None)

	is_private = TRUE
	scm = GIT
	fork_policy = NO_PUBLIC_FORKS
	name = None
	description = None
	has_issues = FALSE
	has_wiki = FALSE

	for repository in repositories:
		new(repository, owner, username, password, is_private, scm, fork_policy, name, description, language, has_issues, has_wiki)


def list(target, name, username = None, password = None, size = False):
	repos = {}
	for repo in lib.bitbucket.list(target, name, username, password):
		repos[repo["full_name"]] = repo["size"]

	if size :
		total = 0
		for key, val in sorted(repos.items(), key = lambda x : -x[1]):
			print(key, lib.bytes.human(val))
			total += val
		print(lib.bytes.human(total))

	else :
		for key in sorted(repos.keys()) : print(key)


def download ( target, name, username = None, password = None, prompt = True, prefix = "", suffix = "", regexp = "" ):

	for repo in lib.bitbucket.list(target, name, username, password):

		slug = repo["full_name"]

		take = True

		take = take and ( not prefix or slug.startswith( prefix ) )
		take = take and ( not suffix or slug.endswith( prefix ) )
		take = take and ( not regexp or re.match( regexp, slug ) is not None )

		if take and ( not prompt or lib.input.yesorno( "clone '%s'?" % slug ) ) :
			clone( slug, username, scm = repo["scm"] )


def get(owner, repo_slug, username = None, password = None):

	if username is not None :
		username, password = lib.config.prompt_cred(DOMAIN, CONFIG_KEY, username, password)

	url = "https://api.bitbucket.org/2.0/repositories/%s/%s" % (owner, repo_slug)

	out, err, p = lib.curl.getjson(url, username = username, password = password, location = True)

	lib.check.SubprocessReturnedFalsyValueException(p.args, p.returncode)

	return json.loads(out.decode())

def exists(owner, repo_slug, username = None, password = None):

	print("error" not in get(owner, repo_slug, username, password))
