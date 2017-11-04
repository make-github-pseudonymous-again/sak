import shutil
import tempfile
import subprocess
import sak.github
import lib.github
import lib.sak
import lib.check
import collections
import lib.dir
import lib.file
import lib.js
import fileinput
import lib.args
import lib.http
from lib.nice.operator import keygetter, keysetter
import os
import json

README = "README.md"

def new(name, subject, keywords=None, username=None, password=None):

    username, password = lib.github.credentials(username, password)

    license, slug, description, fullname, repository, homepage, keywords, fmtargs = lib.js.args(name,subject,keywords,username)

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

    sak.github.clone(repository)

    with lib.dir.cd(slug):

        for basename in os.listdir(lib.sak.data('js')) :
            if os.path.isdir(lib.sak.data('js',basename)):
                shutil.copytree(lib.sak.data('js',basename), basename)
            else:
                shutil.copy(lib.sak.data('js',basename), basename)

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
        lib.git.commit('-am', '$ js new')
        lib.git.push()


def fork(oldrepo, name, subject, keywords=None, username=None, password=None):

    username, password = lib.github.credentials(username, password)

    oldowner, oldslug = oldrepo.split('/')

    license, slug, description, fullname, repository, homepage, keywords, fmtargs = lib.js.args(name,subject,keywords,username)

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

        with open(lib.sak.data('js','package.json'), 'r') as fd:

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
        lib.git.push("-u", "origin", "master")


def deprecated_fromjs(oldrepo, name, subject, keywords=None, username=None, password=None):

    fork(oldrepo, name, subject, keywords=keywords, username=username, password=password)

    license, slug, description, fullname, repository, homepage, keywords, fmtargs = lib.js.args(name,subject,keywords,username)

    es = lib.sak.data('js')

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

        lib.git.add('--all','.')
        lib.git.commit('-a', '-m', '$ js fromjs')
        lib.git.push()

def doc ( ) :

    jsonhook = collections.OrderedDict

    with lib.json.proxy("esdoc.json", "r", object_pairs_hook=jsonhook) as esdoc:
        config = esdoc

    with tempfile.TemporaryDirectory() as tmp:

        tmpconfig = tmp + '/esdoc.json'
        build = tmp + '/build'

        config['destination'] = build

        os.makedirs(build)

        with lib.json.proxy(tmpconfig, "w", object_pairs_hook=jsonhook) as esdoc:
            esdoc.update(config)

        subprocess.run(['npm', 'run', 'esdoc', '--', '-c', tmpconfig],check=True)

        try:

            try:
                lib.git.branch('gh-pages')
            except:
                pass

            lib.git.checkout('gh-pages')

            for basename in os.listdir('.') :
                if basename in ['.git','.gitignore','node_modules'] :
                    pass
                elif os.path.isdir(basename):
                    shutil.rmtree(basename)
                else:
                    os.remove(basename)

            for basename in os.listdir(build) :
                if os.path.isdir(build+'/'+basename):
                    shutil.copytree(build+'/'+basename, basename)
                else:
                    shutil.copy(build+'/'+basename, basename)

            lib.git.add('--all','.')
            lib.git.commit('-a', '-m', 'esdoc update')
            lib.git.push('-u', 'origin', 'gh-pages')

        except:
            raise

        finally:
            lib.git.checkout('master')

def exportall ( cwd = '.' , recursive = False ) :

    with open( '{}/index.js'.format(cwd) , 'w' ) as fd :

        for id , _ in map( os.path.splitext , sorted( os.listdir(cwd) ) ) :

            if id == 'index' : continue

            fd.write( "export * from './{}' ;\n".format( id ) )

    if recursive :

        for directory in filter( os.path.isdir , map( lambda x : '{}/{}'.format( cwd , x ) , os.listdir(cwd) ) ) :

            exportall( cwd = directory , recursive = True)



def exportdefault( cwd = '.' , recursive = False ) :

    with open( '{}/index.js'.format(cwd) , 'w' ) as fd :

        files = map( os.path.splitext , sorted( os.listdir(cwd) ) )

        ids = [ id for id , _ in files if id != 'index' ]

        for id in ids :
            fd.write( "import {0} from './{0}' ;\n".format( id ) )

        fd.write('\n')

        fd.write('export default {\n')
        for id in ids :
            fd.write( "\t{} ,\n".format( id ) )
        fd.write('} ;\n')

        fd.write('\n')

        fd.write('export {\n')
        for id in ids :
            fd.write( "\t{} ,\n".format( id ) )
        fd.write('} ;\n')

    if recursive :

        for directory in filter( os.path.isdir , map( lambda x : '{}/{}'.format( cwd , x ) , os.listdir(cwd) ) ) :

            exportdefault( cwd = directory , recursive = True)



