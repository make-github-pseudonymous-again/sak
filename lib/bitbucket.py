import lib.check, lib.curl, json

DOMAIN = 'bitbucket.org'
CONFIG_KEY = 'bitbucket'

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

USER = "user"
TEAM = "team"

TARGET = "target"
TARGETS = [USER, TEAM]


def list(target, name, username = None, password = None):

	lib.check.OptionNotInListException(TARGET, target, TARGETS)

	if username is not None :
		username, password = lib.config.prompt_cred(DOMAIN, CONFIG_KEY, username, password)

	urls = {
		USER : "https://bitbucket.org/api/2.0/repositories/%s" % name,
		TEAM : "https://bitbucket.org/api/2.0/teams/%s/repositories" % name
	}

	url = urls[target]

	repositories = []

	while True :

		out, err, p = lib.curl.getjson(url, username = username, password = password, location = True)

		lib.check.SubprocessReturnedFalsyValueException(p.args, p.returncode)

		lib.check.SubprocessOutputEmptyException(p.args, out)

		data = json.loads(out.decode())

		repositories.extend(data["values"])

		if not "next" in data : break

		url = data["next"]

	return repositories


LANGUAGES = [
	None,
	"c",
	"c#",
	"c++",
	"html/css",
	"java",
	"javascript",
	"objective-c",
	"perl",
	"php",
	"python",
	"ruby",
	"shell",
	"sql",
	"other",
	"abap",
	"actionscript",
	"ada",
	"arc",
	"apex",
	"asciidoc",
	"android",
	"asp",
	"arduino",
	"assembly",
	"autoit",
	"blitzmax",
	"boo",
	"ceylon",
	"clojure",
	"coco",
	"coffeescript",
	"coldfusion",
	"common lisp",
	"component pascal",
	"css",
	"cuda",
	"d",
	"dart",
	"delphi",
	"duby",
	"dylan",
	"eiffel",
	"elixir",
	"emacs lisp",
	"erlang",
	"euphoria",
	"f#",
	"fantom",
	"forth",
	"fortran",
	"foxpro",
	"gambas",
	"go",
	"groovy",
	"hack",
	"haskell",
	"haxe",
	"igor pro",
	"inform",
	"io",
	"julia",
	"labview",
	"lasso",
	"latex",
	"limbo",
	"livescript",
	"lua",
	"lilypond",
	"m",
	"markdown",
	"mathematica",
	"matlab",
	"max/msp",
	"mercury",
	"nemerle",
	"nimrod",
	"node.js",
	"nu",
	"object pascal",
	"objective-j",
	"ocaml",
	"occam",
	"occam-π",
	"octave",
	"ooc",
	"other",
	"oxygene",
	"pl/sql",
	"powerbasic",
	"powershell",
	"processing",
	"prolog",
	"puppet",
	"pure basic",
	"pure data",
	"qml",
	"quorum",
	"r",
	"racket",
	"realbasic",
	"restructuredtext",
	"rust",
	"sass/scss",
	"scala",
	"scheme",
	"scilab",
	"sclang",
	"self",
	"smalltalk",
	"sourcepawn",
	"standard ml",
	"supercollider",
	"swift",
	"tcl",
	"tex",
	"typescript",
	"unityscript",
	"unrealscript",
	"vala",
	"verilog",
	"vhdl",
	"viml",
	"visual basic",
	"vb.net",
	"xml",
	"xojo",
	"xpages",
	"xquery",
	"xtend",
	"z shell"
]
