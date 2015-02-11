import shutil, sak.github, lib.github, lib.sak, sak.npm
import lib.bower, lib.check, collections, lib.dir, lib.file
import lib.codebricks, fileinput, lib.args, lib.http
import os

TRAVISCI = lib.codebricks.TRAVISCI
DRONEIO = lib.codebricks.DRONEIO
CI = lib.codebricks.CI
FLAT = lib.codebricks.FLAT
SVG = lib.codebricks.SVG
README = "README.md"

def new ( name, subject, keywords = None, ci = TRAVISCI, username = None, password = None ) :

	lib.check.OptionNotInListException("ci", ci, CI)

	username, password = lib.github.credentials(username, password)

	repo = "js-" + name

	description = "%s code bricks for JavaScript" % subject

	fmtargs = dict(name = name, description = description, repo = repo, username = username)

	homepage = "http://%(username)s.github.io/%(repo)s/" % fmtargs
	githubpage = "https://github.com/%(username)s/%(repo)s" % fmtargs
	issuespage = githubpage + "/issues"

	keywords = lib.args.listify( keywords )

	keywords = sorted(list(set(["js", "javascript", "bricks"] + keywords)))

	license = dict(name = "AGPL-3.0", template = "agpl-3.0")

	qualifiedname = "%(username)s-%(repo)s" % fmtargs

	fmtargs["qualifiedname"] = qualifiedname

	sak.github.new(
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

	_, _, p = sak.github.clone( "%(username)s/%(repo)s" % fmtargs, username = username )


	with lib.dir.cd(repo) :

		jsonhook = collections.OrderedDict

		with lib.json.proxy(".groc.json", "w", object_pairs_hook = jsonhook) as groc :
			groc["glob"] = ["js/src/**/*.js", README]
			groc["github"] = True

		with open(".gitignore", "a") as gitignore :
			gitignore.write("\n")
			gitignore.write("# groc\n")
			gitignore.write("doc\n")

		with open(README, "w") as readme :
			readme.write("[%(repo)s](http://%(username)s.github.io/%(repo)s)\n" % fmtargs)
			readme.write("==\n")
			readme.write("\n")
			readme.write("%(description)s\n" % fmtargs)
			readme.write("\n")
			lib.codebricks.badges( username, repo, ci, lambda s : readme.write(s + "\n") )

		with lib.json.proxy("package.json", "w", object_pairs_hook = jsonhook) as npm :
			npm["name"] = qualifiedname
			npm["version"] = "0.0.0"
			npm["description"] = description
			npm["main"] = "js/dist/%(name)s.js" % fmtargs
			npm["dependencies"] = {}
			npm["devDependencies"] = {"aureooms-node-package": "^2.0.3"}
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
				README
			]
			bower["license"] = license["name"]
			bower["homepage"] = homepage

		with lib.json.proxy("component.json", "w", object_pairs_hook = jsonhook) as component :
			component["name"] = qualifiedname
			component["repo"] = "%(username)s/%(repo)s" % fmtargs
			component["version"] = "0.0.0"
			component["license"] = license["name"]
			component["description"] = description
			component["main"] = "js/dist/%(name)s.js" % fmtargs
			component["scripts"] = ["js/dist/%(name)s.js" % fmtargs]

		with lib.json.proxy("pkg.json", "w", object_pairs_hook = jsonhook) as pkg :
			pkg["name"] = name
			pkg["src"] = "js/src/"
			pkg["out"] = "js/dist/"
			pkg["code"] = {}
			pkg["code"]["main"] = ["js", "dist", "%(name)s.js" % fmtargs]
			pkg["code"]["test"] = ["test", "js"]
			pkg["debug"] = False


		lib.dir.makedirs("js/src", "test/js/src")
		lib.file.touch("js/src/dummy.js")

		shutil.copy(lib.sak.data("codebricks", "js-index.js"), "js/index.js")
		shutil.copy(lib.sak.data("codebricks", "test-js-index.js"), "test/js/index.js")
		shutil.copy(lib.sak.data("codebricks", "test-js-src-dummy.js"), "test/js/src/dummy.js")

		if ci == TRAVISCI :
			shutil.copy(lib.sak.data("codebricks", ".travis.yml"), ".travis.yml")

		lib.git.add("--all", ".")
		lib.git.commit("-am", "$ codebricks new")
		lib.git.push()
		sak.npm.install()
		sak.npm.release("0.0.1")
		lib.bower.register(qualifiedname, "github.com/%(username)s/%(repo)s" % fmtargs, force = True)


def badges ( username, repo, ci = TRAVISCI, style = FLAT, fmt = SVG ) :

	lib.codebricks.badges( username, repo, ci, print, style, fmt )


def fork ( oldrepo, name, subject, keywords = None, ci = TRAVISCI, username = None, password = None ) :

	username, password = lib.github.credentials( username, password )

	oldowner, oldslug = oldrepo.split('/')

	slug = "js-" + name

	qualifiedname = "%s-%s" % ( username, slug )

	description = "%s code bricks for JavaScript" % subject

	homepage = "http://%s.github.io/%s/" % ( username, slug )
	githubpage = "https://github.com/%s/%s" % ( username, slug )
	issuespage = githubpage + "/issues"

	keywords = lib.args.listify( keywords )

	keywords = sorted(list(set(["js", "javascript", "bricks"] + keywords)))

	sak.github.new(
		slug,
		username = username,
		password = password,
		auto_init = lib.github.FALSE,
		private = lib.github.FALSE,
		description = description,
		homepage = homepage,
		has_issues = lib.github.TRUE,
		has_wiki = lib.github.TRUE,
		has_downloads = lib.github.TRUE
	)

	sak.github.clone( oldrepo , dest = slug , username = username )

	with lib.dir.cd( slug ) :

		jsonhook = collections.OrderedDict

		for line in fileinput.input( README, inplace = True ) :
			line = line.replace( oldslug, slug )
			line = line.replace( oldowner, username )
			print( line, end = "" )

		with open( README, "a" ) as readme :
			readme.write( "\n" )
			readme.write( "***( forked from [%s](https://github.com/%s) )***" % ( oldslug, oldrepo ) )
			readme.write( "\n" )

		with lib.json.proxy( "package.json", "w", object_pairs_hook = jsonhook ) as npm :
			npm["name"] = qualifiedname
			npm["description"] = description
			npm["main"] = "js/dist/%s.js" % name
			npm["repository"]["url"] = "https://github.com/%s/%s.git" % ( username, slug )
			npm["keywords"] = keywords
			npm["author"] = username
			npm["bugs"]["url"] = issuespage
			npm["homepage"] = homepage

		with lib.json.proxy( "bower.json", "w", object_pairs_hook = jsonhook ) as bower :
			bower["name"] = qualifiedname
			bower["description"] = description
			bower["main"] = "js/dist/%s.js" % name
			bower["homepage"] = homepage

		with lib.json.proxy("component.json", "w", object_pairs_hook = jsonhook) as component :
			component["name"] = qualifiedname
			component["repo"] = "%s/%s" % ( username, slug )
			component["description"] = description
			component["main"] = "js/dist/%s.js" % name
			component["scripts"] = ["js/dist/%s.js" % name]

		with lib.json.proxy( "pkg.json", "w", object_pairs_hook = jsonhook ) as pkg :
			pkg["name"] = name
			pkg["code"]["main"] = ["js", "dist", "%s.js" % name]


		lib.file.rm( "js/dist" )

		url = lib.http.url( "github.com" , path = "%s/%s" % ( username , slug ) , username = username , secure = True )

		lib.git.remote( "set-url", "origin", url )
		lib.git.add( "--all", "." )
		lib.git.commit( "-am", "$ codebricks fork %s" % oldrepo )
		lib.git.push( "-u", "origin", "master" )
		sak.npm.install()
		sak.npm.release( "major" )
		lib.bower.register( qualifiedname, "github.com/%s/%s" % ( username, slug ), force = True )


def component ( qualifiedname , repo , name , version , license , description ) :

	with lib.json.proxy( "component.json" , "w" , object_pairs_hook = collections.OrderedDict ) as component :
		component["name"] = qualifiedname
		component["repo"] = repo
		component["version"] = version
		component["license"] = license
		component["description"] = description
		component["main"] = "js/dist/%s.js" % name
		component["scripts"] = ["js/dist/%s.js" % name]

def usecomponent ( *dirs ) :

	for d in dirs :

		if "component.json" in os.listdir( d ) : continue

		with lib.dir.cd( d ) :

			with lib.json.proxy( "pkg.json" ) as pkg : pass

			with lib.json.proxy( "bower.json" ) as bower : pass

			name = pkg["ns"] if "ns" in pkg else pkg["name"]

			qualifiedname = bower["name"]

			author , *_ = qualifiedname.split("-")

			repo = author + "/js-" + name

			version = bower["version"]

			license = bower["license"]

			description = bower["description"]

			component ( qualifiedname , repo , name , version , license , description )

			lib.git.add( "--all" , "." )
			lib.git.commit( "-am", "add component.json" )
			lib.git.push( )
			sak.npm.release( "patch" )

