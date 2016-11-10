
import os.path
import lib.json
import lib.list
import lib.ver
import lib.git
import lib.args
import collections

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

def args(name,subject,keywords,username):

    license = dict(name="AGPL-3.0", template="agpl-3.0")

    slug = "js-" + name

    description = "{subject} library for JavaScript".format(subject=subject)

    fullname = "{username}-{slug}".format(username=username,slug=slug)
    repository = "{username}/{slug}".format(username=username,slug=slug)
    homepage = "https://{username}.github.io/{slug}".format(username=username,slug=slug)

    keywords = sorted(lib.args.listify(keywords))

    fmtargs = dict(
        name=name,
        description=description,
        slug=slug,
        username=username,
        author=username,
        license=license['name'],
        fullname=fullname,
        repository=repository,
        homepage=homepage,
        keywords=keywords,
        var=name.replace('-','')
    )

    return license, slug, description, fullname, repository, homepage, keywords, fmtargs

