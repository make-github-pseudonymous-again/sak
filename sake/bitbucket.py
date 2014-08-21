import lib.config, lib.git, lib.error, lib.check, subprocess, json

DOMAIN = 'bitbucket.org'
CONFIG_KEY = 'bitbucket'

def clone(what, user = None):

	if user is None : user = lib.config.prompt_user(DOMAIN, CONFIG_KEY)

	lib.git.clone('https://%s@%s/%s.git' % (user, DOMAIN, what))


ALLOW_FORKS = "allow_forks"
NO_PUBLIC_FORKS = "no_public_forks"
NO_FORKS = "no_forks"
FORK_POLICIES = [ALLOW_FORKS, NO_PUBLIC_FORKS, NO_FORKS]

GIT = "git"
HG = "hg"
SCMS = [GIT, HG]

TRUE = "true"
FALSE = "false"
BOOLEANS = [TRUE, FALSE]

LANGUAGES = [None, "c","c#","c++","html/css","java","javascript","objective-c","perl","php","python","ruby","shell","sql","other","abap","actionscript","ada","arc","apex","asciidoc","android","asp","arduino","assembly","autoit","blitzmax","boo","ceylon","clojure","coco","coffeescript","coldfusion","common lisp","component pascal","css","cuda","d","dart","delphi","duby","dylan","eiffel","elixir","emacs lisp","erlang","euphoria","f#","fantom","forth","fortran","foxpro","gambas","go","groovy","hack","haskell","haxe","igor pro","inform","io","julia","labview","lasso","latex","limbo","livescript","lua","lilypond","m","markdown","mathematica","matlab","max/msp","mercury","nemerle","nimrod","node.js","nu","object pascal","objective-j","ocaml","occam","occam-π","octave","ooc","other","oxygene","pl/sql","powerbasic","powershell","processing","prolog","puppet","pure basic","pure data","qml","quorum","r","racket","realbasic","restructuredtext","rust","sass/scss","scala","scheme","scilab","sclang","self","smalltalk","sourcepawn","standard ml","supercollider","swift","tcl","tex","typescript","unityscript","unrealscript","vala","verilog","vhdl","viml","visual basic","vb.net","xml","xojo","xpages","xquery","xtend","z shell"]

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

	if language is None : del parameters["language"]

	jsonparameters = json.dumps(parameters)

	cmd = [
		"curl",
		"-X",
		"POST",
		"-v",
		"-u",
		"%s:%s" % (username, password),
		"-H",
		"Content-Type: application/json",
		"https://api.bitbucket.org/2.0/repositories/%s/%s" % (owner, repository),
		"-d",
		"%s" % (jsonparameters)
	]

	rc = subprocess.call(cmd)
	print()
	lib.check.SubprocessReturnedFalsyValueException(cmd, rc)


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