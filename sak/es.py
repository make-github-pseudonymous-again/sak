import shutil
import sak.github
import lib.github
import lib.sak
import lib.check
import collections
import lib.dir
import lib.file
import lib.es
import fileinput
import lib.args
import lib.http
from lib.nice.operator import keygetter, keysetter
import os
import json

README = "README.md"

def new(name, subject, keywords=None, username=None, password=None):

    username, password = lib.github.credentials(username, password)

    license, slug, description, fullname, repository, homepage, keywords, fmtargs = lib.es.args(name,subject,keywords,username)

    sak.github.new(
        slug,
        username=username,
        password=password,
        auto_init=lib.github.TRUE,
        private=lib.github.FALSE,
        description=description,
        homepage=homepage,
        has_issues=lib.github.TRUE,
        has_wiki=lib.github.TRUE,
        has_downloads=lib.github.TRUE,
        gitignore_template="Node",
        license_template=license["template"]
    )

    _, _, p = sak.github.clone(repository, username=username)

    with lib.dir.cd(slug):

        for basename in os.listdir(lib.sak.data('es')) :
            if os.path.isdir(lib.sak.data('es',basename)):
                shutil.copytree(lib.sak.data('es',basename), basename)
            else:
                shutil.copy(lib.sak.data('es',basename), basename)

        for filename in lib.file.iterall('.',exclude={'./.git'}):

            basename, ext = os.path.splitext(filename)

            _fmtargs = fmtargs

            if ext == '.json' :

                # escape values for json

                _fmtargs = { key: json.dumps( value )[1:-1] for ( key , value ) in fmtargs.items() }

            with open(filename, 'r') as fd:
                data = fd.read()

            data = data.format(**_fmtargs)

            with open(filename, 'w') as fd:
                fd.write(data)

        lib.git.add('--all', '.')
        lib.git.commit('-am', '$ es new')
        lib.git.push()


def fork(oldrepo, name, subject, keywords=None, username=None, password=None):

    username, password = lib.github.credentials(username, password)

    oldowner, oldslug = oldrepo.split('/')

    license, slug, description, fullname, repository, homepage, keywords, fmtargs = lib.es.args(name,subject,keywords,username)

    sak.github.new(
        slug,
        username=username,
        password=password,
        auto_init=lib.github.FALSE,
        private=lib.github.FALSE,
        description=description,
        homepage=homepage,
        has_issues=lib.github.TRUE,
        has_wiki=lib.github.TRUE,
        has_downloads=lib.github.TRUE
    )

    sak.github.clone(oldrepo, dest=slug, username=username)

    with lib.dir.cd(slug):

        jsonhook = collections.OrderedDict

        with open(lib.sak.data('es','package.json'), 'r') as fd:

            # escape json values
            _fmtargs = { key: json.dumps( value )[1:-1] for ( key , value ) in fmtargs.items() }
            _npm = json.loads(fd.read().format(**_fmtargs))

        keys = (
            'name',
            'author',
            'description',
            'keywords',
            'homepage',
            'repository.url',
            'bugs.url'
        )

        new = { key : keygetter(key)(_npm) for key in keys }

        with lib.json.proxy("package.json", "r", object_pairs_hook=jsonhook) as npm:

            old = { key : keygetter(key)(npm) for key in keys }

        old['var'] = old['name'][3:].replace('-','')
        new['var'] = fmtargs['var']

        for filename in lib.file.iterall('.',exclude={'./.git'}):

            basename, ext = os.path.splitext(filename)

            _old, _new = old, new

            if ext == '.json' :

                # escape values for json

                _old = { key: json.dumps( value )[1:-1] for ( key , value ) in old.items() }
                _new = { key: json.dumps( value )[1:-1] for ( key , value ) in new.items() }


            with open(filename, 'r') as fd:
                data = fd.read()

            for key in keys :
                data.replace(str(_old[key]),str(_new[key]))

            with open(filename, 'w') as fd:
                fd.write(data)

        url = lib.http.url("github.com", path=repository, username=username, secure=True)

        lib.git.remote("set-url", "origin", url)
        lib.git.add("--all", ".")
        lib.git.commit("-am", "$ es fork {}".format( oldrepo ) )
        lib.git.push("-u", "origin", "master")


def fromjs(oldrepo, name, subject, keywords=None, username=None, password=None):

    fork(oldrepo, name, subject, keywords=keywords, username=username, password=password)

    license, slug, description, fullname, repository, homepage, keywords, fmtargs = lib.es.args(name,subject,keywords,username)

    es = lib.sak.data('es')

    with lib.dir.cd(slug):

        for filename in lib.file.iterall(es):

            basename, ext = os.path.splitext(filename)

            _fmtargs = fmtargs

            if ext == '.json' :

                # escape values for json

                _fmtargs = { key: json.dumps( value )[1:-1] for ( key , value ) in fmtargs.items() }

            with open(filename,'r') as fd :
                data = fd.read()

            data = data.format(**_fmtargs)

            new = filename[len(es)+1:]

            if new == 'README.md' and os.path.exists(new):
                data += '\n\n# OLD README BELOW\n\n'
                with open(new,'r') as fd :
                    data += fd.read()

            if os.path.dirname(new):
                os.makedirs(os.path.dirname(new),exist_ok=True)

            with open(new,'w') as fd :
                fd.write(data)


        for filename in ( '.groc.json', 'inch.json' , 'pkg.json', 'component.json', 'bower.json' ) :
            try:
                os.remove(filename)
            except:
                pass

