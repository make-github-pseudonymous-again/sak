import lib.config
import lib.git
import lib.error
import lib.check
import lib.github
import lib.input
import lib.http
import lib.args
import lib.json
import sys
import re
import json

DOMAIN = lib.github.DOMAIN
CONFIG_KEY = lib.github.CONFIG_KEY
LICENSES = lib.github.LICENSES
GITIGNORES = lib.github.GITIGNORES
TRUE = lib.github.TRUE
FALSE = lib.github.FALSE
BOOLEANS = lib.github.BOOLEANS
YOU = lib.github.YOU
NEWEST = lib.github.NEWEST
OLDEST = lib.github.OLDEST
STARGAZERS = lib.github.STARGAZERS
SORT = lib.github.SORT


def clone(repo, dest=None, asuser=None, **kwargs):

    if asuser is not None:
        url = lib.http.url(DOMAIN, repo, asuser, secure=True)
    else:
        url = 'gh:{}'.format(repo)

    if dest is not None:
        return lib.git.clone(url, dest, **kwargs)
    else:
        return lib.git.clone(url, **kwargs)


def new(name, org=None, team_id=None, token=None, auto_init=FALSE, private=FALSE, description=None, homepage=None, has_issues=TRUE, has_wiki=TRUE, has_downloads=TRUE, gitignore_template=None, license_template=None):

    lib.check.OptionNotInListException("private", private, BOOLEANS)
    lib.check.OptionNotInListException("has_issues", has_issues, BOOLEANS)
    lib.check.OptionNotInListException("has_wiki", has_wiki, BOOLEANS)
    lib.check.OptionNotInListException(
        "has_downloads", has_downloads, BOOLEANS)
    lib.check.OptionNotInListException("auto_init", auto_init, BOOLEANS)
    lib.check.OptionNotInListException(
        "gitignore_template", gitignore_template, GITIGNORES)
    lib.check.OptionNotInListException(
        "license_template", license_template, LICENSES)

    token = lib.github.pat(token)

    parameters = {
        "name": name,
        "description": description,
        "homepage": homepage,
        "private": private,
        "has_issues": has_issues,
        "has_wiki": has_wiki,
        "has_downloads": has_downloads,
        "team_id": team_id,
        "auto_init": auto_init,
        "gitignore_template": gitignore_template,
        "license_template": license_template
    }

    if org is None:
        url = ("user", "repos")
    else:
        url = ("orgs", org, "repos")

    lib.github.post(url, data=parameters, token=token, stddefault=None)
    print()


def group(*names):

    token = lib.github.pat(None)

    org = None
    team_id = None
    auto_init = FALSE
    private = FALSE
    description = None
    homepage = None
    has_issues = TRUE
    has_wiki = TRUE
    has_downloads = TRUE
    gitignore_template = None
    license_template = None

    for name in names:
        new(name, org, team_id, token, auto_init, private, description,
            homepage, has_issues, has_wiki, has_downloads, gitignore_template, license_template)


def list(target=YOU, name=None, t=None, format="{full_name}", token=None):

    for repo in lib.github.list(target, name, t, token):
        print(format.format(**repo))

def download(target=YOU, name=None, t=None, token=None, prompt=True, prefix="", suffix="", regexp="", asuser=None, **kwargs):

    for repo in lib.github.list(target, name, t, token):

        repo = repo["full_name"]

        take = True

        take = take and (not prefix or repo.startswith(prefix))
        take = take and (not suffix or repo.endswith(suffix))
        take = take and (not regexp or re.match(regexp, repo) is not None)

        if take and (not prompt or lib.input.yesorno("clone '%s'?" % repo)):
            clone(repo, asuser=asuser, **kwargs)


def delete(owner, repo, token=None):
    token = lib.github.pat(token)

    url = ("repos", owner, repo)
    lib.github.delete(url, token=token, stddefault=None)
    print()

def transfer(owner, repo, new_owner, token=None):

    token = lib.github.pat(token)

    url = ("repos", owner, repo, "transfer")
    parameters = { "new_owner": new_owner }
    lib.github.post(url, data=parameters, token=token, stddefault=None)
    print()

def search(what, query, token=None, **kwargs):

    response = lib.args.forward(lib.github.search, locals())

    for result in response:
        try:
            items = result['items']
            if not items: break
            for item in items:
                json.dump(item, sys.stdout)
        except:
            json.dump(result, sys.stderr)
            break


def issues(owner=None, repo=None, number=None, user=False, org=None, token=None, milestone=None, filter=None, state=None, creator=None, assignee=None, mentioned=None, labels=None, sort=None, direction=None, since=None):

    for issue in lib.args.forward(lib.github.issues, locals()):
        lib.json.oneline(issue, sys.stdout)

def createissue(owner, repo, title, body=None, assignee=None, milestone=None, labels=None, token=None):

    print(lib.args.forward(lib.github.createissue, locals()))


def editissue(owner, repo, number, title=None, body=None, assignee=None, state=None, milestone=None, labels=None, token=None):

    print(lib.args.forward(lib.github.editissue, locals()))


def closeissues(owner, repo, *issuenos, token=None):

    for response in lib.args.forward(lib.github.closeissues, locals()):

        print(response)


def comments(owner, repo, id=None, number=None, sort=None, direction=None, since=None, token=None):

    print(lib.args.forward(lib.github.comments, locals()))


def createcomment(owner, repo, number, body, token=None):

    print(lib.args.forward(lib.github.createcomment, locals()))


def editcomment(owner, repo, id, body, token=None):

    print(lib.args.forward(lib.github.editcomment, locals()))


def deletecomment(owner, repo, id, token=None):

    print(lib.args.forward(lib.github.deletecomment, locals()))


def labels(owner, repo, name=None, issue=None, token=None):

    print(lib.args.forward(lib.github.labels, locals()))


def createlabel(owner, repo, name, color, token=None):

    print(lib.args.forward(lib.github.createlabel, locals()))


def updatelabel(owner, repo, oldname, newname, color, token=None):

    print(lib.args.forward(lib.github.updatelabel, locals()))


def deletelabel(owner, repo, name, token=None):

    print(lib.args.forward(lib.github.deletelabel, locals()))


def addlabels(owner, repo, issue, labels=None, token=None):

    print(lib.args.forward(lib.github.addlabels, locals()))


def removelabel(owner, repo, issue, label, token=None):

    print(lib.args.forward(lib.github.removelabel, locals()))


def updatelabels(owner, repo, issue, labels=None, token=None):

    print(lib.args.forward(lib.github.updatelabels, locals()))


def removealllabels(owner, repo, issue, token=None):

    print(lib.args.forward(lib.github.removealllabels, locals()))


def milestonelabels(owner, repo, milestone, token=None):

    print(lib.args.forward(lib.github.milestonelabels, locals()))


def milestones(owner, repo, number=None, state=None, sort=None, direction=None, token=None):

    print(lib.args.forward(lib.github.milestones, locals()))


def createmilestone(owner, repo, title, state=None, description=None, due_on=None, token=None):

    print(lib.args.forward(lib.github.createmilestone, locals()))


def updatemilestone(owner, repo, number, title, state=None, description=None, due_on=None, token=None):

    print(lib.args.forward(lib.github.updatemilestone, locals()))


def deletemilestone(owner, repo, number, token=None):

    print(lib.args.forward(lib.github.deletemilestone, locals()))


def listforks(owner, repo, sort=NEWEST, token=None, identify=False):
    """
            https://developer.github.com/v3/issues/labels/
    """

    if identify:
        token = lib.github.pat(token)

    url = ("repos", owner, repo, "forks")

    parameters = dict(sort=sort)

    lib.github.get(url, data=parameters, token=token, stddefault=None)
    print()


def fork(owner, repo, organization=None, token=None):
    """
            https://developer.github.com/v3/issues/labels/
    """

    token = lib.github.pat(token)

    url = ("repos", owner, repo, "forks")

    parameters = dict(organization=organization)

    lib.github.post(url, data=parameters, token=token, stddefault=None)
    print()


def patch(owner, repo, name, token=None, private=FALSE, description=None, homepage=None, has_issues=TRUE, has_wiki=TRUE, has_downloads=TRUE, default_branch=None):

    lib.check.OptionNotInListException("private", private, BOOLEANS)
    lib.check.OptionNotInListException("has_issues", has_issues, BOOLEANS)
    lib.check.OptionNotInListException("has_wiki", has_wiki, BOOLEANS)
    lib.check.OptionNotInListException(
        "has_downloads", has_downloads, BOOLEANS)

    token = lib.github.pat(token)

    parameters = {
        "name": name,
        "description": description,
        "homepage": homepage,
        "private": private,
        "has_issues": has_issues,
        "has_wiki": has_wiki,
        "has_downloads": has_downloads,
        "default_branch": default_branch
    }

    url = ("repos", owner, repo)

    lib.github.patch(url, data=parameters, token=token, stddefault=None)
    print()

# WEBHOOKS


def listhooks(owner, repo, token=None):

    for hook in lib.args.forward(lib.github.listhooks, locals()):

        print(hook)


def getsinglehook(owner, repo, id, token=None):

    print(lib.args.forward(lib.github.getsinglehook, locals()))


def createhook(owner, repo, url, name="web", content_type="json", secret=None, insecure_ssl="0", events="push", active=True, token=None):

    print(lib.args.forward(lib.github.createhook, locals()))

# LONG PROCEDURES


def archive(username, forks=False, gist=True, metadata=True):
    """
            All credits go to Filippo Valsorda (https://filippo.io).

            original -> https://filippo.io/archive-your-github-repo-and-data/

            # This is free and unencumbered software released into the public domain.

            # Anyone is free to copy, modify, publish, use, compile, sell, or
            # distribute this software, either in source code form or as a compiled
            # binary, for any purpose, commercial or non-commercial, and by any
            # means.

            # In jurisdictions that recognize copyright laws, the author or authors
            # of this software dedicate any and all copyright interest in the
            # software to the public domain. We make this dedication for the benefit
            # of the public at large and to the detriment of our heirs and
            # successors. We intend this dedication to be an overt act of
            # relinquishment in perpetuity of all present and future rights to this
            # software under copyright law.

            # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
            # EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
            # MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
            # IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
            # OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
            # ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
            # OTHER DEALINGS IN THE SOFTWARE.

            # For more information, please refer to <http://unlicense.org/>

            usage: gh_dump.py [-h] [--forks] [--no-gist] [--no-metadata] username

            Dump an user's public GitHub data into current directory.

            positional arguments:
            username the GH username

            optional arguments:
            -h, --help show this help message and exit
            --forks git clone also forks (default is don't)
            --no-gist don't download user gists (default is do)
            --no-metadata don't download user metadata (default is do)
    """

    from urllib.request import urlopen
    from subprocess import call
    import json
    import re
    import os.path

    def clear_url(url):
        return re.sub(r'\{[^\}]*\}', '', url)

    data = urlopen('https://api.github.com/users/' + args.user).read()
    user = json.loads(data.decode('utf-8'))
    if args.metadata:
        with open('user.json', 'wb') as f:
            f.write(data)

    data = urlopen(clear_url(user['repos_url'])).read()
    repos = json.loads(data.decode('utf-8'))
    if args.metadata:
        with open('repos.json', 'wb') as f:
            f.write(data)
    for repo in repos:
        if not repo['fork']:
            call(['git', 'clone', repo['clone_url']])
        elif args.forks:
            if not os.path.exists('forks'):
                os.makedirs('forks')
            call(['git', 'clone', repo['clone_url'],
                  os.path.join('forks', repo['name'])])

    data = urlopen(clear_url(user['gists_url'])).read()
    gists = json.loads(data.decode('utf-8'))
    if args.metadata:
        with open('gists.json', 'wb') as f:
            f.write(data)
    if args.gists:
        if not os.path.exists('gists'):
            os.makedirs('gists')
        for gist in gists:
            call(['git', 'clone', gist['git_pull_url'],
                  os.path.join('gists', gist['id'])])

    if args.metadata:
        for name in ['received_events', 'events', 'organizations', 'followers', 'starred', 'following', 'subscriptions']:
            data = urlopen(clear_url(user[name + '_url'])).read()
            with open(name + '.json', 'wb') as f:
                f.write(data)


def migrateissues(owner, origin, destination, *issuenos, token=None):

    token = lib.github.pat(token)

    print("fetch issues to migrate")

    issuestomigrate = []

    for number in issuenos:

        out = lib.github.issues(owner, origin, number, token=token)

        lib.github.validate(out)

        issuestomigrate.append(out)

    print("compute labels and milestones to migrate")

    labelstomigrate = {}

    milestonestomigrate = {}

    for issue in issuestomigrate:

        if "labels" in issue and issue["labels"] is not None:

            for label in issue["labels"]:

                labelstomigrate.setdefault(label["name"], label)

        if "milestone" in issue and issue["milestone"] is not None:

            milestone = issue["milestone"]

            milestonestomigrate.setdefault(milestone["title"], milestone)

    print("remove already existing labels from the migrate list")

    labelsalreadythere = lib.github.labels(
        owner, destination, token=token)

    lib.github.validate(labelsalreadythere)

    for label in labelsalreadythere:

        labelstomigrate.pop(label["name"], None)

    print("remove already existing milestones from the migrate list and save them to map")

    milestonesmap = {}

    milestonesalreadythere = lib.github.milestones(
        owner, destination, token=token)

    lib.github.validate(milestonesalreadythere)

    for milestone in milestonesalreadythere:

        title = milestone["title"]

        milestonefrom = milestonestomigrate.get(title, None)

        if milestonefrom is not None:

            milestonesmap[milestonefrom["number"]] = milestone["number"]

            milestonestomigrate.pop(title)

    print("migrate labels")

    for name, label in labelstomigrate.items():

        color = label["color"]

        lib.github.validate(lib.github.createlabel(
            owner, destination, name, color, token=token))

    print("migrate milestones and save map between old numbers and new ones")

    for title, milestone in milestonestomigrate.items():

        parameters = lib.dict.select(
            milestone, ["state", "description", "due_on"])

        number = milestone["number"]

        out = lib.github.createmilestone(
            owner, destination, title, token=token, **parameters)

        lib.github.validate(out)

        milestonesmap[number] = out["number"]

    print("migrate issues and save map between old numbers and new ones")

    issuemap = {}

    for issue in issuestomigrate:

        parameters = {}

        if "milestone" in issue and issue["milestone"] is not None:

            number = issue["milestone"]["number"]

            parameters["milestone"] = milestonesmap[number]

        if "labels" in issue and issue["labels"] is not None:

            parameters["labels"] = [label["name"] for label in issue["labels"]]

        if "assignee" in issue and issue["assignee"] is not None:

            parameters["assignee"] = issue["assignee"]["login"]

        if "body" in issue and issue["body"] is not None:

            parameters["body"] = issue["body"]

        title = issue["title"]

        out = lib.github.createissue(
            owner, destination, title, token=token, **parameters)

        lib.github.validate(out)

        issuemap[issue["number"]] = out

    print("fetch comments if necessary")

    commentstomigrate = {}

    for issue in issuestomigrate:

        if "comments" in issue and issue["comments"] > 0:

            number = issue["number"]

            commentstomigrate[number] = lib.github.comments(
                owner, origin, number=number, token=token)

            lib.github.validate(commentstomigrate[number])

    print("migrate comments")

    for number, listofcomments in commentstomigrate.items():

        number = issuemap[number]["number"]

        for comment in listofcomments:

            body = comment["body"]

            lib.github.validate(lib.github.createcomment(
                owner, destination, number, body, token=token))

    print("add comment to say that it was migrated to destination")
    print("add comment to say that it was migrated from origin")

    for issuefrom in issuestomigrate:

        numberfrom = issuefrom["number"]

        issueto = issuemap[numberfrom]

        numberto = issueto["number"]

        bodyfrom = "migrated to %s" % issueto["html_url"]

        bodyto = "migrated from %s" % issuefrom["html_url"]

        lib.github.validate(lib.github.createcomment(
            owner, origin, numberfrom, bodyfrom, token=token))

        lib.github.validate(lib.github.createcomment(
            owner, destination, numberto, bodyto, token=token))

    print("close issues from origin")

    for issue in issuestomigrate:

        parameters = {}

        parameters["title"] = issue.get("title", None)

        parameters["body"] = issue.get("body", None)

        parameters["state"] = "closed"

        if "assignee" in issue and issue["assignee"] is not None:
            parameters["assignee"] = issue["assignee"]["login"]

        if "milestone" in issue and issue["milestone"] is not None:
            parameters["milestone"] = issue["milestone"]["number"]

        if "labels" in issue and issue["labels"] is not None:
            parameters["labels"] = [label["name"] for label in issue["labels"]]

        lib.github.validate(lib.github.editissue(owner, origin, issue[
                            "number"], token=token, **parameters))


def notifications(all=False, participating=False, since=None, before=None, token=None):

    response = lib.args.forward(lib.github.notifications, locals())

    for result in response:
        lib.json.oneline(result, sys.stdout)

def mark_as_read(thread_id, token=None):

    print(lib.args.forward(lib.github.mark_as_read, locals()))

def license(license_template, key='body', token=None):
    license = lib.github.license(license_template, token=token)
    output = license[key]
    sys.stdout.write(output)
