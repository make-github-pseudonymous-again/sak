
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
from itertools import chain

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

def args(name, subject, keywords, username, org, slugprefix='', fullnameprefix='@{scope}/', subjectsuffix=' for JavaScript', license_template="agpl-3.0", version='0.0.0', emoji=None, scope=None, author=None, packageType='module'):

    license = lib.github.license(license_template)

    slug = slugprefix + name

    description = subject + subjectsuffix
    github_description = description if emoji is None else '{} {}'.format(emoji, description)

    owner = org or username
    if scope is None: scope = owner
    if author is None: author = username
    fullname = (fullnameprefix + "{slug}").format(scope=scope,slug=slug)
    repository = "{owner}/{slug}".format(owner=owner,slug=slug)
    homepage = "https://{owner}.github.io/{slug}".format(owner=owner,slug=slug)

    commonjsExtension = 'js' if packageType == 'commonjs' else 'cjs'
    moduleExtension = 'js' if packageType == 'module' else 'mjs'

    keywords = sorted(lib.args.listify(keywords))

    var = make_var(name)

    fmtargs = dict(
        name=fullname,
        description=description,
        readme_heading_prefix='' if emoji is None else '{} '.format(emoji),
        version=version,
        license=license['spdx_id'],
        author=author,
        repository=repository,
        homepage=homepage,
        keywords=keywords,
        var=var,
        packageType=packageType,
        commonjsExtension=commonjsExtension,
        moduleExtension=moduleExtension,
    )

    return license, slug, description, github_description, repository, homepage, keywords, fmtargs

def entrypoints(cwd, entrypoint):
    # Goes recursive if entrypoint is None
    with os.scandir(cwd) as entries:
        yield from chain.from_iterable(
            map(
                lambda x:
                    [x.name] if x.is_file() else
                    map(lambda y: '{}/{}'.format(x.name, y),
                        entrypoints('{}/{}'.format(cwd, x.name), None)) if
                    entrypoint is None else
                    ['{}/{}'.format(x.name, entrypoint)],
                sorted(
                    filter(
                        lambda x: x.name != entrypoint,
                        entries
                    ),
                    key = lambda x: (x.is_file(), x.name)
                )
            )
        )

def entrypoint_id(filename, entrypoint):
    entrypoint_suffix = '/' + entrypoint
    if filename.endswith(entrypoint_suffix):
        path = filename[:-len(entrypoint_suffix)]
    else:
        path = os.path.splitext(filename)[0]
    return path.split('/')[-1]
