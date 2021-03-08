
import os
import lib.json
import lib.list
import lib.ver
import lib.git
import lib.check
import lib.github
import lib.args
import collections
import re

NPM = 'package.json'
BOWER = 'bower.json'

PM = [NPM, BOWER]

VERSION_HASH = 'version'


def unique(versions):
    if not versions:
        return None

    lib.check.VersionNotUniqueException(versions)

    version = next(iter(versions.values()))
    return version


def readpackagefiles():

    versions = {}
    for pm in PM:
        with lib.json.proxy(pm, 'r', default={}) as conf:
            if VERSION_HASH in conf:
                old = conf[VERSION_HASH]
                lib.check.OldSemverVersionTagNotValidException(old, pm)
                versions[pm] = old

    return versions


def writeversion(version, files=PM):

    hook = collections.OrderedDict

    for pm in files:
        with lib.json.proxy(pm, 'w', object_pairs_hook=hook) as conf:
            conf[VERSION_HASH] = version


def getversion():
    versions = readpackagefiles()
    return unique(versions)


def setversion(version):

    olds = readpackagefiles()
    old = unique(olds)

    if lib.ver.isspecial(version):
        lib.check.CannotInferSemverVersionNumberException(old, version)
        version = lib.ver.resolve(old, version)

    else:
        lib.check.SemverVersionTagNotValidException(version)
        lib.check.NewSemverVersionTagNotGreaterException(version, old)

    writeversion(version, files=olds.keys())

    return version


def upload(version, message=None):
    version = lib.ver.PREFIX + version
    if message is None:
        message = version

    lib.git.add('--all', '.')
    lib.git.commit('-am', message)
    lib.git.pull()
    lib.git.push()
    lib.git.tag('-a', version, '-m', message)
    lib.git.push('--tags')

def make_var(name):
    return re.sub('^[A-Z]', lambda match: match.group(0).lower(), name.title().replace('-',''))

def args(name,subject,keywords,username,slugprefix='js-',fullnameprefix='@{username}/', subjectsuffix=' for JavaScript', license_template="agpl-3.0", version='0.0.0', emoji=None):

    license = lib.github.license(license_template)

    slug = slugprefix + name

    description = subject + subjectsuffix
    github_description = description if emoji is None else '{} {}'.format(emoji, description)

    fullname = (fullnameprefix + "{slug}").format(username=username,slug=slug)
    repository = "{username}/{slug}".format(username=username,slug=slug)
    homepage = "https://{username}.github.io/{slug}".format(username=username,slug=slug)

    keywords = sorted(lib.args.listify(keywords))

    var = make_var(name)

    fmtargs = dict(
        name=fullname,
        description=description,
        readme_heading_prefix='' if emoji is None else '{} '.format(emoji),
        version=version,
        license=license['spdx_id'],
        author=username,
        repository=repository,
        homepage=homepage,
        keywords=keywords,
        var=var
    )

    return license, slug, description, github_description, fullname, repository, homepage, keywords, fmtargs

def entrypoints(cwd, entrypoint):
    with os.scandir(cwd) as entries:
        yield from map(
            lambda x: x.name if x.is_file() else '{}/{}'.format(x.name, entrypoint),
            sorted(
                filter(
                    lambda x: x.name != entrypoint,
                    entries
                ),
                key = lambda x: (x.is_file(), x.name)
            )
        )
