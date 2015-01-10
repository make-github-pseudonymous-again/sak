# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import lib.config, lib.git, lib.error, lib.check, json, lib.curl, lib.url


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


def api ( *args ) :

	return "https://api.github.com/" + '/'.join( map( str , args ) )


def credentials ( username = None , password = None ) :

	return lib.config.prompt_cred( DOMAIN , CONFIG_KEY , username , password )


def paginate ( url , username = None , password = None ) :

	username , password = credentials( username , password )

	pageid = 1

	while True :

		pageurl = url + lib.url.get( page = str( pageid ) )

		out , err , p = lib.curl.getjson( pageurl , username = username , password = password )

		lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )

		pagecontent = json.loads( out.decode() )

		if not pagecontent : break

		yield pagecontent

		pageid += 1


def itemize ( url , username = None , password = None ) :

	for page in paginate( url , username = username , password = password ) :

		for item in page : yield item


def list ( target = YOU, name = None, t = None, username = None, password = None ) :

	lib.check.OptionNotInListException( TARGET, target, TARGETS )

	if t is None : t = TYPES_DEFAULT[target]
	lib.check.OptionNotInListException( TYPE, t, TYPES[target] )

	if target == YOU or t == PRIVATE or username is not None :
		username , password = credentials( username , password )

	if   target ==  YOU : url = api( "user" , "repos" )
	elif target == USER : url = api( "users" , name , "repos" )
	elif target ==  ORG : url = api( "orgs" , name , "repos" )

	return itemize( url , username = username , password = password )


def issues( owner = None , repo = None , user = False, org = None, username = None, password = None, filter = None, state = None, labels = None, sort = None, direction = None, since = None ) :

	"""
		https://developer.github.com/v3/issues/
	"""

	username , password = credentials( username , password )

	if owner is not None and repo is not None :
		url = api( "repos" , owner , repo , "issues" )
	elif user :
		url = api( "user" , "issues" )
	elif org is not None :
		url = api( "orgs" , org , "issues" )
	else :
		url = api( "issues" )

	parameters = {
		"filter" : filter,
		"state" : state,
		"labels" : labels,
		"sort": sort,
		"direction" : direction,
		"since" : since
	}

	out , err , p = lib.curl.getjson(url, parameters, username, password, accept = "application/vnd.github.v3.raw+json" )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )

	return json.loads( out.decode() )


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

NEWEST = "newest"
OLDEST = "oldest"
STARGAZERS = "stargazers"

SORT = [ NEWEST, OLDEST, STARGAZERS ]
