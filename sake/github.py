import lib.config, lib.git, lib.error, lib.check, subprocess, json

DOMAIN = 'github.com'
CONFIG_KEY = 'github'

def clone(what, user = None):

	if user is None : user = lib.config.prompt_user(DOMAIN, 'github')

	lib.git.clone('https://%s@%s/%s.git' % (user, DOMAIN, what))


LICENSES = [
	None,
	"agpl-3.0",
	"apache-2.0",
	"artistic-2.0",
	"bsd-2-clause",
	"bsd-3-clause",
	"cc0",
	"epl-1.0",
	"gpl-2.0",
	"gpl-3.0",
	"isc",
	"lgpl-2.1",
	"lgpl-3.0",
	"mit",
	"mpl-2.0",
	"no-license",
	"unlicense"
]

GITIGNORES = [
	None,
	"Actionscript",
	"Ada",
	"Agda",
	"Android",
	"AppceleratorTitanium",
	"ArchLinuxPackages",
	"Autotools",
	"Bancha",
	"CakePHP",
	"CFWheels",
	"C",
	"C++",
	"ChefCookbook",
	"Clojure",
	"CMake",
	"CodeIgniter",
	"CommonLisp",
	"Composer",
	"Concrete5",
	"Coq",
	"Dart",
	"Delphi",
	"DM",
	"Drupal",
	"Eagle",
	"Elisp",
	"Elixir",
	"EPiServer",
	"Erlang",
	"ExpressionEngine",
	"ExtJS-MVC",
	"Fancy",
	"Finale",
	"ForceDotCom",
	"Fortran",
	"FuelPHP",
	"gcov",
	"Go",
	"Gradle",
	"Grails",
	"GWT",
	"Haskell",
	"Idris",
	"Java",
	"Jboss",
	"Jekyll",
	"Joomla",
	"Jython",
	"Kohana",
	"LabVIEW",
	"Laravel4",
	"Leiningen",
	"LemonStand",
	"Lilypond",
	"Lithium",
	"Magento",
	"Maven",
	"Mercury",
	"MetaProgrammingSystem",
	"Meteor",
	"nanoc",
	"Node",
	"Objective-C",
	"OCaml",
	"Opa",
	"OpenCart",
	"OracleForms",
	"Packer",
	"Perl",
	"Phalcon",
	"PlayFramework",
	"Plone",
	"Prestashop",
	"Processing",
	"Python",
	"Qooxdoo",
	"Qt",
	"Rails",
	"R",
	"RhodesRhomobile",
	"ROS",
	"Ruby",
	"Rust",
	"Sass",
	"Scala",
	"SCons",
	"Scrivener",
	"Sdcc",
	"SeamGen",
	"SketchUp",
	"stella",
	"SugarCRM",
	"Swift",
	"Symfony2",
	"Symfony",
	"SymphonyCMS",
	"Target3001",
	"Tasm",
	"TeX",
	"Textpattern",
	"TurboGears2",
	"Typo3",
	"Umbraco",
	"Unity",
	"VisualStudio",
	"VVVV",
	"Waf",
	"WordPress",
	"Yeoman",
	"Yii",
	"ZendFramework",
	"Zephir"
]


TRUE = True
FALSE = False
BOOLEANS = [TRUE, FALSE]

def new(name, org = None, team_id = None, username = None, password = None, auto_init = FALSE, private = FALSE, description = None, homepage = None, has_issues = TRUE, has_wiki = TRUE, has_downloads = TRUE, gitignore_template = None, license_template = None):

	lib.check.OptionNotInListException("private", private, BOOLEANS)
	lib.check.OptionNotInListException("has_issues", has_issues, BOOLEANS)
	lib.check.OptionNotInListException("has_wiki", has_wiki, BOOLEANS)
	lib.check.OptionNotInListException("has_downloads", has_downloads, BOOLEANS)
	lib.check.OptionNotInListException("auto_init", auto_init, BOOLEANS)
	lib.check.OptionNotInListException("gitignore_template", gitignore_template, GITIGNORES)
	lib.check.OptionNotInListException("license_template", license_template, LICENSES)

	username, password = lib.config.prompt_cred(DOMAIN, CONFIG_KEY, username, password)


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

	jsonparameters = json.dumps(parameters)


	if org is None :
		url = "https://api.github.com/user/repos"
	else :
		url = "https://api.github.com/orgs/%s/repos" % org

	cmd = [
		"curl",
		"-X",
		"POST",
		"-v",
		"-u",
		"%s:%s" % (username, password),
		"-H",
		"Content-Type: application/json",
		url,
		"-d",
		"%s" % (jsonparameters)
	]

	rc = subprocess.call(cmd)
	print()
	lib.check.SubprocessReturnedFalsyValueException(cmd, rc)

