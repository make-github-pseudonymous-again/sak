from __future__ import absolute_import, division, print_function, unicode_literals

import os, shutil, sake.github, lib.github, lib.sake, sake.npm, lib.bower, lib.check, collections

TRAVISCI = "travis-ci"
DRONEIO = "drone.io"

CI = [TRAVISCI, DRONEIO]

def new(name, subject, keywords = None, ci = TRAVISCI, username = None, password = None):

	lib.check.OptionNotInListException("ci", ci, CI)

	username, password = lib.github.credentials(username, password)

	repo = "js-" + name

	description = "%s code bricks for JavaScript" % subject

	fmtargs = dict(name = name, description = description, repo = repo, username = username)

	homepage = "http://%(username)s.github.io/%(repo)s/" % fmtargs
	githubpage = "https://github.com/%(username)s/%(repo)s" % fmtargs
	issuespage = "https://github.com/%(username)s/%(repo)s/issues" % fmtargs

	if keywords is None : keywords = []

	keywords = sorted(list(set(["js", "javascript", "bricks"] + keywords)))

	license = dict(name = "AGPL-3.0", template = "agpl-3.0")

	qualifiedname = "%(username)s-%(repo)s" % fmtargs

	sake.github.new(
		repo,
		username = username,
		password = password,
		auto_init = lib.github.TRUE,
		private = lib.github.FALSE,
		description = description,
		homepage = homepage,
		has_issues = lib.github.TRUE,
		has_wiki = lib.github.TRUE,
		has_downloads = lib.github.TRUE,
		gitignore_template = "Node",
		license_template = license["template"]
	)


	_, _, p = sake.github.clone("%(username)s/%(repo)s" % fmtargs, username)

	os.chdir(repo)

	try :

		jsonhook = collections.OrderedDict

		with lib.json.proxy(".groc.json", "w", object_pairs_hook = jsonhook) as groc :
			groc["glob"] = ["js/src/**/*.js", "README.md"]
			groc["github"] = True

		with open(".gitignore", "a") as gitignore :
			gitignore.write("\n")
			gitignore.write("# groc\n")
			gitignore.write("doc\n")

		with open("README.md", "w") as readme :
			readme.write("[%(repo)s](http://%(username)s.github.io/%(repo)s)\n" % fmtargs)
			readme.write("==\n")
			readme.write("\n")
			readme.write("%(description)s\n" % fmtargs)
			readme.write("\n")
			if ci == TRAVISCI :
				readme.write("[![Build Status](https://travis-ci.org/%(username)s/%(repo)s.svg)](https://travis-ci.org/%(username)s/%(repo)s)\n" % fmtargs)
			elif ci == DRONEIO :
				readme.write("[![Build Status](https://drone.io/github.com/%(username)s/%(repo)s/status.png)](https://drone.io/github.com/%(username)s/%(repo)s/latest)\n" % fmtargs)
			readme.write("[![Coverage Status](https://coveralls.io/repos/%(username)s/%(repo)s/badge.png)](https://coveralls.io/r/%(username)s/%(repo)s)\n" % fmtargs)
			readme.write("[![Dependencies Status](https://david-dm.org/%(username)s/%(repo)s.png)](https://david-dm.org/%(username)s/%(repo)s#info=dependencies)\n" % fmtargs)
			readme.write("[![devDependencies Status](https://david-dm.org/%(username)s/%(repo)s/dev-status.png)](https://david-dm.org/%(username)s/%(repo)s#info=devDependencies)\n" % fmtargs)
			readme.write("[![Code Climate](https://codeclimate.com/github/%(username)s/%(repo)s.png)](https://codeclimate.com/github/%(username)s/%(repo)s)\n" % fmtargs)

		with lib.json.proxy("package.json", "w", object_pairs_hook = jsonhook) as npm :
			npm["name"] = qualifiedname
			npm["version"] = "0.0.0"
			npm["description"] = description
			npm["main"] = "js/dist/%(name)s.js" % fmtargs
			npm["dependencies"] = {}
			npm["devDependencies"] = {"aureooms-node-package": "^1.0.0"}
			npm["scripts"] = {}
			npm["scripts"]["build"] = "./node_modules/.bin/aureooms-node-package-build"
			npm["scripts"]["test"] = "./node_modules/.bin/aureooms-node-package-test"
			npm["scripts"]["doc"] = "./node_modules/.bin/groc"
			npm["repository"] = {}
			npm["repository"]["type"] = "git"
			npm["repository"]["url"] = "https://github.com/%(username)s/%(repo)s.git" % fmtargs
			npm["keywords"] = keywords
			npm["author"] = username
			npm["license"] = license["name"]
			npm["bugs"] = {}
			npm["bugs"]["url"] = issuespage
			npm["homepage"] = homepage


		with lib.json.proxy("bower.json", "w", object_pairs_hook = jsonhook) as bower :
			bower["name"] = qualifiedname
			bower["version"] = "0.0.0"
			bower["description"] = description
			bower["main"] = "js/dist/%(name)s.js" % fmtargs
			bower["ignore"] = [
				"js/index.js",
				"js/src",
				"test",
				"pkg.json",
				"package.json",
				".groc.json",
				".travis.yml",
				".gitignore",
				"README.md"
			]
			bower["license"] = license["name"]
			bower["homepage"] = homepage

		with lib.json.proxy("pkg.json", "w", object_pairs_hook = jsonhook) as pkg :
			pkg["ns"] = name
			pkg["src"] = "js/src/"
			pkg["out"] = "js/dist/"
			pkg["code"] = {}
			pkg["code"]["main"] = ["js", "dist", "%(name)s.js" % fmtargs]
			pkg["code"]["test"] = ["test", "js"]
			pkg["debug"] = False

		os.mkdir("js")
		os.mkdir("js/src")
		os.mkdir("test")
		os.mkdir("test/js")
		os.mkdir("test/js/src")

		shutil.copy(lib.sake.data("codebricks", "js-index.js"), "js/index.js")
		shutil.copy(lib.sake.data("codebricks", "test-js-index.js"), "test/js/index.js")
		if ci == TRAVISCI :
			shutil.copy(lib.sake.data("codebricks", ".travis.yml"), ".travis.yml")

		lib.git.add("--all", ".")
		lib.git.commit("-am", "$ codebricks new")
		lib.git.push()
		sake.npm.install()
		sake.npm.release("0.0.1")
		lib.bower.register(qualifiedname, "github.com/%(username)s/%(repo)s" % fmtargs, force = True)

	finally :
		os.chdir("..")
