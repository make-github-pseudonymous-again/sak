"""
	Exposes Github API v3.
"""


import json , functools
import lib.fn , lib.args
import lib.config, lib.git, lib.error, lib.check, lib.curl, lib.url , lib.dict

# CONSTANTS

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



# TOOLS

def api ( *args ) :
	return "https://api.github.com/" + '/'.join( map( str , args ) )

@lib.fn.throttle( 20 , 70 )
def send ( method , url , data = None , **kwargs ) :

	"""
		Throttling because
		https://github.com/octokit/octokit.net/issues/638#issuecomment-67795998
	"""

	contenttype = "application/json"

	if data is not None :
		data = json.dumps(data)

	return lib.curl.call( method , api( *url ) , contenttype , data = data , **kwargs )

put = functools.partial( send , lib.curl.PUT )
get = functools.partial( send , lib.curl.GET )
post = functools.partial( send , lib.curl.POST )
update = functools.partial( send , lib.curl.UPDATE )
patch = functools.partial( send , lib.curl.PATCH )
delete = functools.partial( send , lib.curl.DELETE )


def credentials ( username = None , password = None ) :

	return lib.config.prompt_cred( DOMAIN , CONFIG_KEY , username , password )


def paginate ( url , username = None , password = None ) :

	username , password = credentials( username , password )

	pageid = 1

	while True :

		pageurl = url[:-1] + ( url[-1] + lib.url.get( page = str( pageid ) ) , )

		out , err , p = get( pageurl , username = username , password = password )

		lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )

		pagecontent = json.loads( out.decode() )

		if not pagecontent : break

		yield pagecontent

		pageid += 1


def itemize ( url , username = None , password = None ) :

	for page in paginate( url , username = username , password = password ) :

		for item in page : yield item


def validate ( data ) :

	if "message" in data :

		msg = data["message"]

		if "errors" in data :

			for i , err in enumerate( data["errors"] ) :

				msg += "\n#" + str( i ) + " -> " + json.dumps( err )

		raise lib.error.GithubAPIException( msg )



# REPOS

def list ( target = YOU, name = None, t = None, username = None, password = None ) :

	lib.check.OptionNotInListException( TARGET, target, TARGETS )

	if t is None : t = TYPES_DEFAULT[target]
	lib.check.OptionNotInListException( TYPE, t, TYPES[target] )

	if target == YOU or t == PRIVATE or username is not None :
		username , password = credentials( username , password )

	if   target ==  YOU : url = ( "user" , "repos" )
	elif target == USER : url = ( "users" , name , "repos" )
	elif target ==  ORG : url = ( "orgs" , name , "repos" )

	return itemize( url , username = username , password = password )



# ISSUES

def issues ( owner = None , repo = None , number = None , user = False , org = None , username = None , password = None , milestone = None , filter = None , state = None , creator = None , assignee = None , mentioned = None , labels = None , sort = None , direction = None , since = None ) :

	"""
		https://developer.github.com/v3/issues/
	"""

	username , password = credentials( username , password )

	if owner is not None and repo is not None :
		if number is None :
			url = ( "repos" , owner , repo , "issues" )
		else :
			url = ( "repos" , owner , repo , "issues" , number )
	elif user :
		url = ( "user" , "issues" )
	elif org is not None :
		url = ( "orgs" , org , "issues" )
	else :
		url = ( "issues" , )

	keys = [ "milestone" , "filter" , "state" , "assignee" , "creator" , "mentioned" , "labels" , "sort" , "direction" , "since" ]

	parameters = lib.dict.select( locals( ) , keys )

	out , err , p = get( url , data = parameters , username = username , password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )

	return json.loads( out.decode( ) )


def closeissues ( owner , repo , *issuenos , username = None , password = None ) :

	username , password = credentials( username , password )

	for number in issuenos :

		issue = issues( owner , repo , number , username = username , password = password )

		keys = [ "title" , "body" , "assignee" , "milestone" , "labels" ]

		parameters = lib.dict.select( issue , keys )

		parameters["state"] = "closed"

		yield editissue( owner , repo , number , username = username , password = password , **parameters )


def createissue ( owner , repo , title , body = None , assignee = None , milestone = None , labels = None , username = None , password = None ) :

	"""
		https://developer.github.com/v3/issues/#create-an-issue
	"""

	url = ( "repos" , owner , repo , "issues" )

	labels = lib.args.listify( labels )

	keys = [ "title" , "body" , "assignee" , "milestone" , "labels" ]

	parameters = lib.dict.select( locals( ) , keys )

	username , password = credentials( username , password )

	out , err , p = post( url , data = parameters , username = username , password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )

	return json.loads( out.decode( ) )


def editissue ( owner , repo , number , title = None , body = None , assignee = None , state = None , milestone = None , labels = None , username = None , password = None ) :

	"""
		https://developer.github.com/v3/issues/#edit-an-issue
	"""

	url = ( "repos" , owner , repo , "issues" , number )

	labels = lib.args.listify( labels )

	keys = [ "title" , "body" , "assignee" , "state" , "milestone" , "labels" ]

	parameters = lib.dict.select( locals( ) , keys )

	username , password = credentials( username , password )

	out , err , p = patch( url , data = parameters , username = username , password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )
	return json.loads( out.decode( ) )



# LABELS

def labels ( owner, repo, name = None, issue = None, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	if issue is not None :
		url = ( "repos", owner, repo, "issues", issue, "labels" )
	elif name is not None :
		url = ( "repos", owner, repo, "labels", name )
	else :
		url = ( "repos", owner, repo, "labels" )

	out , err , p = get( url, username = username, password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )
	return json.loads( out.decode( ) )


def createlabel ( owner, repo, name, color, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	url = ( "repos", owner, repo, "labels" )

	parameters = lib.dict.select( locals( ) , [ "name" , "color" ] )

	username , password = credentials( username , password )

	out , err , p = post(url, data = parameters, username = username, password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )
	return json.loads( out.decode( ) )


def updatelabel ( owner, repo, oldname, newname, color, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	url = ( "repos", owner, repo, "labels", oldname )

	parameters = dict( name = newname, color = color )

	username, password = credentials( username, password )

	out , err , p = patch( url, data = parameters, username = username, password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )
	return json.loads( out.decode( ) )



def deletelabel ( owner, repo, name, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	url = ( "repos", owner, repo, "labels", name )

	username, password = credentials( username, password )

	out , err , p = delete( url, username = username, password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )
	return json.loads( out.decode( ) )


def addlabels ( owner, repo, issue, labels = None, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	labels = lib.args.listify( labels )

	username, password = credentials( username, password )

	url = ( "repos", owner, repo, "issues", issue, "labels" )

	out , err , p = post( url, data = labels, username = username, password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )
	return json.loads( out.decode( ) )


def removelabel ( owner, repo, issue, label, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	username, password = credentials( username, password )

	url = ( "repos", owner, repo, "issues", issue, "labels", label )

	out , err , p = delete( url, username = username, password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )
	return json.loads( out.decode( ) )


def updatelabels ( owner, repo, issue, labels = None, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	labels = lib.args.listify( labels )

	username, password = credentials( username, password )

	url = ( "repos", owner, repo, "issues", issue, "labels" )

	out , err , p = put( url, data = labels, username = username, password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )
	return json.loads( out.decode( ) )


def removealllabels ( owner, repo, issue, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	username, password = credentials( username, password )

	url = ( "repos", owner, repo, "issues", issue, "labels" )

	out , err , p = delete( url, username = username, password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )
	return json.loads( out.decode( ) )


def milestonelabels ( owner, repo, milestone, username = None, password = None ) :

	"""
		https://developer.github.com/v3/issues/labels/
	"""

	url = ( "repos", owner, repo, "milestones", milestone, "labels" )

	out , err , p = get( url, username = username, password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args, p.returncode )
	return json.loads( out.decode( ) )



# MILESTONES

def milestones ( owner , repo , number = None , state = None , sort = None , direction = None , username = None , password = None ) :

	if number is None :
		url = ( "repos" , owner , repo , "milestones" )
	else :
		url = ( "repos" , owner , repo , "milestones" , number )

	parameters = lib.dict.select( locals( ) , [ "state" , "sort" , "direction" ] )

	username , password = credentials( username , password )

	out , err , p = get( url , data = parameters , username = username , password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args , p.returncode )
	return json.loads( out.decode( ) )


def createmilestone ( owner , repo , title , state = None , description = None , due_on = None , username = None , password = None ) :

	url = ( "repos" , owner , repo , "milestones" )

	parameters = lib.dict.select( locals( ) , [ "title" , "state" , "description" , "due_on" ] )

	username , password = credentials( username , password )

	out , err , p = post( url , data = parameters , username = username , password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args , p.returncode )
	return json.loads( out.decode( ) )


def updatemilestone ( owner , repo , number , title , state = None , description = None , due_on = None , username = None , password = None ) :

	url = ( "repos" , owner , repo , "milestones" , number )

	parameters = lib.dict.select( locals( ) , [ "title" , "state" , "description" , "due_on" ] )

	username , password = credentials( username , password )

	out , err , p = patch( url , data = parameters , username = username , password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args , p.returncode )
	return json.loads( out.decode( ) )


def deletemilestone ( owner , repo , number , username = None , password = None ) :

	url = ( "repos" , owner , repo , "milestones" , number )

	username , password = credentials( username , password )

	out , err , p = delete( url , username = username , password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args , p.returncode )
	return json.loads( out.decode( ) )



# COMMENTS

def comments ( owner , repo , id = None , number = None , sort = None , direction = None , since = None , username = None , password = None ) :

	if id is not None :
		url = ( "repos" , owner , repo , "issues" , "comments" , id )
	elif number is None :
		url = ( "repos" , owner , repo , "issues" , "comments" )
	else :
		url = ( "repos" , owner , repo , "issues" , number , "comments" )

	parameters = lib.dict.select( locals( ) , [ "sort" , "direction" , "since" ] )

	username , password = credentials( username , password )

	out , err , p = get( url , data = parameters , username = username , password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args , p.returncode )
	return json.loads( out.decode( ) )


def createcomment ( owner , repo , number , body , username = None , password = None ) :

	url = ( "repos" , owner , repo , "issues" , number , "comments" )

	parameters = lib.dict.select( locals( ) , [ "body" ] )

	username , password = credentials( username , password )

	out , err , p = post( url , data = parameters , username = username , password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args , p.returncode )
	return json.loads( out.decode( ) )


def editcomment ( owner , repo , id , body , username = None , password = None ) :

	url = ( "repos" , owner , repo , "issues" , "comments" , id )

	parameters = lib.dict.select( locals( ) , [ "body" ] )

	username , password = credentials( username , password )

	out , err , p = patch( url , data = parameters , username = username , password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args , p.returncode )
	return json.loads( out.decode( ) )


def deletecomment ( owner , repo , id , username = None , password = None ) :

	url = ( "repos" , owner , repo , "issues" , "comments" , id )

	username , password = credentials( username , password )

	out , err , p = delete( url , username = username , password = password )
	lib.check.SubprocessReturnedFalsyValueException( p.args , p.returncode )
	return json.loads( out.decode( ) )





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
