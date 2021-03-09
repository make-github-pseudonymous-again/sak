"""
	Exposes Github API v3.
"""

import sys
import json
import functools
import lib.fn
import lib.args
import lib.passwordstore
import lib.git
import lib.error
import lib.check
import lib.curl
import lib.url
import lib.dict

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
TYPES_ORG = [ALL, PUBLIC, PRIVATE, FORKS, SOURCES, MEMBER]

TYPES = {
    YOU: TYPES_YOU,
    USER: TYPES_USER,
    ORG: TYPES_ORG
}

TYPES_DEFAULT = {
    YOU: ALL,
    USER: OWNER,
    ORG: ALL
}

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

SORT = [NEWEST, OLDEST, STARGAZERS]

# TOOLS


def api(path, params):
    return "https://api.github.com/" + '/'.join(map(str, path)) + lib.url.get(**params)

def _safe ( value ) :

    if value is True : return 'true'
    if value is False : return 'false'

    return value

@lib.fn.throttle(20, 70)
def send(method, url, params=dict(), data=None, token=None, **kwargs):
    """
            Throttling because
            https://github.com/octokit/octokit.net/issues/638#issuecomment-67795998
    """

    contenttype = "application/vnd.github.v3+json"

    if data is not None:
        data = json.dumps(data)

    safe_params = {key: _safe(value) for key, value in params.items() if value is not None}

    queryurl = api(url, safe_params)

    print(queryurl, file=sys.stderr)

    authorization = None if token is None else 'token {}'.format(token)

    out, err, p = lib.curl.call(method, queryurl, contenttype, data=data, authorization=authorization, **kwargs)

    lib.check.SubprocessReturnedFalsyValueException(p.args, p.returncode)

    return json.loads(out.decode()) if out else None


put = functools.partial(send, lib.curl.PUT)
get = functools.partial(send, lib.curl.GET)
post = functools.partial(send, lib.curl.POST)
update = functools.partial(send, lib.curl.UPDATE)
patch = functools.partial(send, lib.curl.PATCH)
delete = functools.partial(send, lib.curl.DELETE)


def pat ( token = None ) :
    if token is not None : return token
    return lib.passwordstore.get('apps/github/pat')

def paginate(url, token=None, **kwargs):

    pageid = 1
    PER_PAGE_MAX = 100

    while True:

        params = dict(page=str(pageid), per_page=str(PER_PAGE_MAX), **kwargs)

        pagecontent = get(url, params=params, token=token)

        if not pagecontent:
            break

        validate(pagecontent)
        yield pagecontent

        pageid += 1


def itemize(url, **kwargs):

    for page in paginate(url, **kwargs):

        for item in page:
            yield item


def validate(data):

    if "message" in data:

        raise lib.error.GithubAPIException(data)


# REPOS

def list(target=YOU, name=None, t=None, token=None):

    lib.check.OptionNotInListException(TARGET, target, TARGETS)

    if t is None:
        t = TYPES_DEFAULT[target]
    lib.check.OptionNotInListException(TYPE, t, TYPES[target])

    if target == YOU or t == PRIVATE: token = pat(token)

    if target == YOU:
        url = ("user", "repos")
    elif target == USER:
        url = ("users", name, "repos")
    elif target == ORG:
        url = ("orgs", name, "repos")

    return itemize(url, token=token)


# ISSUES

def issues(owner=None, repo=None, number=None, user=False, org=None, token=None, filter=None, state=None, labels=None, sort=None, direction=None, since=None):
    """
            https://developer.github.com/v3/issues/
    """

    token = pat(token)

    if owner is not None and repo is not None:
        if number is None:
            url = ("repos", owner, repo, "issues")
        else:
            url = ("repos", owner, repo, "issues", number)
    elif user:
        url = ("user", "issues")
    elif org is not None:
        url = ("orgs", org, "issues")
    else:
        url = ("issues", )

    keys = ["filter", "state",
            "labels", "sort", "direction", "since"]

    params = lib.dict.select(locals(), keys)

    if number:
        return [get(url, token=token, params=params)]
    else:
        return itemize(url, token=token, **params)



def search ( what , query , token=None, **kwargs ) :

    """
        https://developer.github.com/v3/search
    """

    url = ("search", what)
    # params = { 'q': query }
    # yield get(url, params=params, token=token)
    return paginate(url, q=query, token=token, **kwargs)


def closeissues(owner, repo, *issuenos, token=None):

    token = pat(token)

    for number in issuenos:

        issue = issues(owner, repo, number,
                       token=token)

        keys = ["title", "body", "assignee", "milestone", "labels"]

        parameters = lib.dict.select(issue, keys)

        parameters["state"] = "closed"

        yield editissue(owner, repo, number, token=token, **parameters)


def createissue(owner, repo, title, body=None, assignee=None, milestone=None, labels=None, token=None):
    """
            https://developer.github.com/v3/issues/#create-an-issue
    """

    url = ("repos", owner, repo, "issues")

    labels = lib.args.listify(labels)

    keys = ["title", "body", "assignee", "milestone", "labels"]

    parameters = lib.dict.select(locals(), keys)

    token = pat(token)

    return post(url, data=parameters, token=token)


def editissue(owner, repo, number, title=None, body=None, assignee=None, state=None, milestone=None, labels=None, token=None):
    """
            https://developer.github.com/v3/issues/#edit-an-issue
    """

    url = ("repos", owner, repo, "issues", number)

    labels = lib.args.listify(labels)

    keys = ["title", "body", "assignee", "state", "milestone", "labels"]

    parameters = lib.dict.select(locals(), keys)

    token = pat(token)

    return patch(url, data=parameters, token=token)

# LABELS

def labels(owner, repo, name=None, issue=None, token=None):
    """
            https://developer.github.com/v3/issues/labels/
    """

    if issue is not None:
        url = ("repos", owner, repo, "issues", issue, "labels")
    elif name is not None:
        url = ("repos", owner, repo, "labels", name)
    else:
        url = ("repos", owner, repo, "labels")

    return get(url, token=token)


def createlabel(owner, repo, name, color, token=None):
    """
            https://developer.github.com/v3/issues/labels/
    """

    url = ("repos", owner, repo, "labels")

    parameters = lib.dict.select(locals(), ["name", "color"])

    token = pat(token)

    return post(url, data=parameters, token=token)


def updatelabel(owner, repo, oldname, newname, color, token=None):
    """
            https://developer.github.com/v3/issues/labels/
    """

    url = ("repos", owner, repo, "labels", oldname)

    parameters = dict(name=newname, color=color)

    token = pat(token)

    return patch(url, data=parameters, token=token)


def deletelabel(owner, repo, name, token=None):
    """
            https://developer.github.com/v3/issues/labels/
    """

    url = ("repos", owner, repo, "labels", name)

    token = pat(token)

    return delete(url, token=token)


def addlabels(owner, repo, issue, labels=None, token=None):
    """
            https://developer.github.com/v3/issues/labels/
    """

    labels = lib.args.listify(labels)

    token = pat(token)

    url = ("repos", owner, repo, "issues", issue, "labels")

    return post(url, data=labels, token=token)


def removelabel(owner, repo, issue, label, token=None):
    """
            https://developer.github.com/v3/issues/labels/
    """

    token = pat(token)

    url = ("repos", owner, repo, "issues", issue, "labels", label)

    return delete(url, token=token)


def updatelabels(owner, repo, issue, labels=None, token=None):
    """
            https://developer.github.com/v3/issues/labels/
    """

    labels = lib.args.listify(labels)

    token = pat(token)

    url = ("repos", owner, repo, "issues", issue, "labels")

    return put(url, data=labels, token=token)


def removealllabels(owner, repo, issue, token=None):
    """
            https://developer.github.com/v3/issues/labels/
    """

    token = pat(token)

    url = ("repos", owner, repo, "issues", issue, "labels")

    return delete(url, token=token)


def milestonelabels(owner, repo, milestone, token=None):
    """
            https://developer.github.com/v3/issues/labels/
    """

    url = ("repos", owner, repo, "milestones", milestone, "labels")

    return get(url, token=token)


# MILESTONES

def milestones(owner, repo, number=None, state=None, sort=None, direction=None, token=None):

    if number is None:
        url = ("repos", owner, repo, "milestones")
    else:
        url = ("repos", owner, repo, "milestones", number)

    parameters = lib.dict.select(locals(), ["state", "sort", "direction"])

    token = pat(token)

    return get(url, data=parameters, token=token)


def createmilestone(owner, repo, title, state=None, description=None, due_on=None, token=None):

    url = ("repos", owner, repo, "milestones")

    parameters = lib.dict.select(
        locals(), ["title", "state", "description", "due_on"])

    token = pat(token)

    return post(url, data=parameters, token=token)


def updatemilestone(owner, repo, number, title, state=None, description=None, due_on=None, token=None):

    url = ("repos", owner, repo, "milestones", number)

    parameters = lib.dict.select(
        locals(), ["title", "state", "description", "due_on"])

    token = pat(token)

    return patch(url, data=parameters, token=token)


def deletemilestone(owner, repo, number, token=None):

    url = ("repos", owner, repo, "milestones", number)

    token = pat(token)

    return delete(url, token=token)


# COMMENTS

def comments(owner, repo, id=None, number=None, sort=None, direction=None, since=None, token=None):

    if id is not None:
        url = ("repos", owner, repo, "issues", "comments", id)
    elif number is None:
        url = ("repos", owner, repo, "issues", "comments")
    else:
        url = ("repos", owner, repo, "issues", number, "comments")

    parameters = lib.dict.select(locals(), ["sort", "direction", "since"])

    token = pat(token)

    return get(url, data=parameters, token=token)


def createcomment(owner, repo, number, body, token=None):

    url = ("repos", owner, repo, "issues", number, "comments")

    parameters = lib.dict.select(locals(), ["body"])

    token = pat(token)

    return post(url, data=parameters, token=token)


def editcomment(owner, repo, id, body, token=None):

    url = ("repos", owner, repo, "issues", "comments", id)

    parameters = lib.dict.select(locals(), ["body"])

    token = pat(token)

    return patch(url, data=parameters, token=token)


def deletecomment(owner, repo, id, token=None):

    url = ("repos", owner, repo, "issues", "comments", id)

    token = pat(token)

    return delete(url, token=token)


# WEBHOOKS

def listhooks(owner, repo, token=None):

    url = ("repos", owner, repo, "hooks")

    token = pat(token)

    return itemize(url, token=token)


def getsinglehook(owner, repo, id, token=None):

    url = ("repos", owner, repo, "hooks", id)

    token = pat(token)

    return get(url, token=token)


def createhook(owner, repo, url, name="web", content_type="json", secret=None, insecure_ssl="0", events="push", active=True, token=None):

    events = lib.args.listify(events)

    apiurl = ("repos", owner, repo, "hooks")

    config = lib.dict.select(
        locals(), ["url", "content_type", "secret", "insecure_ssl"])

    parameters = lib.dict.select(
        locals(), ["name", "config", "events", "active"])

    token = pat(token)

    return post(apiurl, data=parameters, token=token)

# NOTIFICATIONS

def notifications(all=False, participating=False, since=None, before=None, token=None):

    # all 	boolean 	If true, show notifications marked as read. Default: false
    # participating 	boolean 	If true, only shows notifications in which the user is directly participating or mentioned. Default: false
    # since 	string 	Only show notifications updated after the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.
    # before 	string 	Only show notifications updated before the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.

    token = pat(token)

    url = ("notifications",)

    return itemize(url, all=all, participating=participating, since=since, before=before, token=token)

def mark_as_read (thread_id, token=None):

    """
        https://developer.github.com/v3/activity/notifications/#mark-a-thread-as-read
    """

    token = pat(token)

    url = ("notifications", "threads", thread_id)

    return patch(url, token=token)


def license(license_template, token=None):
    token = pat(token)
    path = ("licenses", license_template)
    return get(path, token=token)
