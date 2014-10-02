from __future__ import absolute_import, division, print_function, unicode_literals

import lib.config, lib.git, lib.error, lib.check, json, lib.curl


DOMAIN = 'github.com'
CONFIG_KEY = 'github'

YOU = "you"
USER = "user"
ORG = "org"

TARGET = "target"
TARGETS = [YOU, USER, ORG]

ALL = "all"
OWNER = "owner"
PUBLIC = "public"
PRIVATE = "private"
MEMBER = "member"
FORKS = "forks"
SOURCES = "sources"

TYPE = "t"
TYPES_YOU = [ALL, OWNER, PUBLIC, PRIVATE, MEMBER]
TYPES_USER = [ALL, OWNER, MEMBER]
TYPES_ORG  = [ALL, PUBLIC, PRIVATE, FORKS, SOURCES, MEMBER]

TYPES = {
	YOU : TYPES_YOU,
	USER : TYPES_USER,
	ORG  : TYPES_ORG
}

TYPES_DEFAULT = {
	YOU : ALL,
	USER : OWNER,
	ORG  : ALL
}


def credentials(username = None, password = None):
	return lib.config.prompt_cred(DOMAIN, CONFIG_KEY, username, password)

def list(target = YOU, name = None, t = None, username = None, password = None):

	lib.check.OptionNotInListException(TARGET, target, TARGETS)

	if t is None : t = TYPES_DEFAULT[target]
	lib.check.OptionNotInListException(TYPE, t, TYPES[target])

	if target == YOU or t == PRIVATE or username is not None :
		username, password = credentials(username, password)

	urls = {
		YOU : "https://api.github.com/user/repos",
		USER : "https://api.github.com/users/%s/repos" % name,
		ORG  : "https://api.github.com/orgs/%s/repos" % name
	}


	url = urls[target]

	out, err, p = lib.curl.getjson(url, username = username, password = password)

	lib.check.SubprocessReturnedFalsyValueException(p.args, p.returncode)

	return json.loads(out.decode())


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
