import shutil
import sak.github
import lib.git
import lib.json
import lib.github
import lib.sak
import lib.check
import collections
import lib.dir
import lib.file
import lib.js
import lib.args
import lib.http
from lib.nice.operator import keygetter
import os
import sys
import json
import re
from difflib import unified_diff

README = "README.md"

def new(name, subject, keywords=None, username=None, token=None, **rest):

    license, slug, description, github_description, fullname, repository, homepage, keywords, fmtargs = lib.js.args(name,subject,keywords,username,**rest)

    sak.github.new(
        slug,
        token=token,
        auto_init=lib.github.FALSE,
        private=lib.github.FALSE,
        description=github_description,
        homepage=homepage,
        has_issues=lib.github.TRUE,
        has_wiki=lib.github.TRUE,
        has_downloads=lib.github.TRUE
    )

    sak.github.clone(repository)

    with lib.dir.cd(slug):

        for entry in os.scandir(lib.sak.data('js')):
            if entry.is_dir():
                shutil.copytree(lib.sak.data('js',entry.name), entry.name)
            else:
                shutil.copy(lib.sak.data('js',entry.name), entry.name)

        with open('LICENSE', 'w') as fd:
            fd.write(license['body'])

        for filename in lib.file.iterall('.',exclude={'./.git'}):

            _fmtargs = fmtargs
            _, ext = os.path.splitext(filename)
            if ext == '.json' :
                _fmtargs = encode_json_values(_fmtargs)

            with open(filename, 'r') as fd:
                data = fd.read()

            data = data.format(**_fmtargs)
            if ext == '.json':
                # pretty-print json
                data = json.dumps(json.loads(data), indent = 2)+'\n'

            with open(filename, 'w') as fd:
                fd.write(data)

        lib.git.add('--all')
        lib.git.commit('--message', ':robot: chore: Setup repository.')
        lib.git.push('-u', 'origin', 'main')


def fork(oldrepo, name, subject, keywords=None, username=None, token=None, **rest):

    license, slug, description, github_description, fullname, repository, homepage, keywords, fmtargs = lib.js.args(name,subject,keywords,username, **rest)

    sak.github.new(
        slug,
        token=token,
        auto_init=lib.github.FALSE,
        private=lib.github.FALSE,
        description=github_description,
        homepage=homepage,
        has_issues=lib.github.TRUE,
        has_wiki=lib.github.TRUE,
        has_downloads=lib.github.TRUE
    )

    sak.github.clone(oldrepo, dest=slug)

    with lib.dir.cd(slug):

        jsonhook = collections.OrderedDict

        with open(lib.sak.data('js','package.json'), 'r') as fd:
            _fmtargs = encode_json_values(fmtargs)
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

            _old, _new = old, new
            _, ext = os.path.splitext(filename)
            if ext == '.json' :
                _old = encode_json_values(_old)
                _new = encode_json_values(_new)

            try:
                with open(filename, 'r') as fd:
                    data = fd.read()

                for key in keys :
                    data.replace(str(_old[key]),str(_new[key]))

                with open(filename, 'w') as fd:
                    fd.write(data)

            except UnicodeDecodeError:
                pass

        url = lib.http.url("github.com", path=repository, username=username, secure=True)

        lib.git.remote("set-url", "origin", url)
        lib.git.push("--set-upstream", "origin", "main")


def deprecated_fromjs(oldrepo, name, subject, keywords=None, username=None, token=None, **rest):

    fork(oldrepo, name, subject, keywords=keywords, username=username, token=token, **rest)

    license, slug, description, github_description, fullname, repository, homepage, keywords, fmtargs = lib.js.args(name,subject,keywords,username, **rest)

    es = lib.sak.data('js')

    with lib.dir.cd(slug):

        for filename in lib.file.iterall(es):

            _fmtargs = fmtargs
            _, ext = os.path.splitext(filename)
            if ext == '.json' :
                _fmtargs = encode_json_values(_fmtargs)

            with open(filename,'r') as fd :
                data = fd.read()

            data = data.format(**_fmtargs)
            if ext == '.json':
                # pretty-print json
                data = json.dumps(json.loads(data), indent = 2)+'\n'

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

        lib.git.add('--all')
        lib.git.commit('--message', '$ js fromjs')
        lib.git.push()


def exportall ( cwd = '.' , recursive = False , entrypoint = 'index.js' ) :

    filenames = list(lib.js.entrypoints(cwd, entrypoint))

    with open( os.path.join(cwd, entrypoint) , 'w' ) as fd :

        for filename in filenames :

            fd.write( "export * from './{}';\n".format( filename ) )

    if recursive :
        for directory in lib.dir.directories(cwd) :
            exportall( cwd = directory , recursive = True, entrypoint = entrypoint)



def exportdefault( cwd = '.' , recursive = False , entrypoint = 'index.js', named=True, default=False ) :

    filenames = list(lib.js.entrypoints(cwd, entrypoint))

    with open( os.path.join(cwd, entrypoint) , 'w' ) as fd :

        ids = list(map(lambda x: os.path.splitext(x)[0], filenames))

        for [id, filename] in zip(ids, filenames) :
            fd.write( "import {0} from './{1}';\n".format( id, filename ) )

        fd.write('\n')

        if default:
            fd.write('/* eslint import/no-anonymous-default-export: [2, {"allowObject": true}] */\n')
            fd.write('export default {\n')
            for id in ids :
                fd.write( "\t{},\n".format( id ) )
            fd.write('};\n')

            fd.write('\n')

        if named:
            fd.write('export {\n')
            for id in ids :
                fd.write( "\t{},\n".format( id ) )
            fd.write('};\n')

    if recursive :
        for directory in lib.dir.directories(cwd) :
            exportdefault( cwd = directory , recursive = True, entrypoint = entrypoint, named=False, default=True)


def encode_json_values ( obj ):
    literal = { key: json.dumps( value ) for ( key , value ) in obj.items() }
    raw = { '_'+key: value[1:-1] for ( key , value ) in literal.items() }
    return {**literal, **raw}


def diff(cwd = '.'):

    with lib.json.proxy(os.path.join(cwd, "package.json"), "r") as package:
        name = package['name']
        description = package['description']
        version = package['version']
        license = package['license']
        author = package['author']
        homepage = package['homepage'].rstrip('/')
        repository = '/'.join(package['repository']['url'].split('/')[3:])
        if repository[-4:] == '.git': repository = repository[:-4]
        keywords = package['keywords']

    emoji = None

    with open(os.path.join(cwd, 'README.md')) as fd:
        readme_heading = fd.readline()
        m = re.match(r"(:[^:]+:) \[", readme_heading)
        if m:
            emoji = m.group(1)

    var = lib.js.make_var(name.split('/')[-1])
    with open(os.path.join(cwd, 'doc', 'manual', 'usage.md'), 'r') as fd:
        for line in fd:
            m = re.match(r"const ([a-zA-Z]\w*) = require", line)
            if m:
                var = m.group(1)
                break

    fmtargs = dict(
        name=name,
        description=description,
        readme_heading_prefix='' if emoji is None else '{} '.format(emoji),
        version=version,
        license=license,
        author=author,
        homepage=homepage,
        repository=repository,
        keywords=keywords,
        var=var
    )

    with lib.dir.cd(cwd):

        root = lib.sak.data('js')

        for absfilename in lib.file.iterall(root,exclude={'./.git'}):
            relfilename = absfilename[len(root)+1:]
            if not os.path.isfile(relfilename):
                print('! removed {}'.format(relfilename), file=sys.stderr)

        for filename in lib.file.iterall('.',exclude={'./.git'}):

            if filename.startswith('./node_modules/'): continue
            if filename.startswith('./coverage/'): continue
            if filename.startswith('./dist/'): continue
            if filename.startswith('./lib/'): continue
            if filename.startswith('./src/'): continue
            if filename.startswith('./test/'): continue
            if filename.startswith('./.husky/_/'): continue
            if filename == './LICENSE': continue
            if filename == './yarn.lock': continue

            template = lib.sak.data('js', filename)

            if not os.path.isfile(template):
                print('! added {}'.format(filename), file=sys.stderr)
                continue

            _fmtargs = fmtargs
            _, ext = os.path.splitext(filename)
            if ext == '.json' :
                _fmtargs = encode_json_values(_fmtargs)

            with open(template, 'r') as fd:
                data = fd.read().format(**_fmtargs)
                if ext == '.json':
                    # pretty-print json
                    data = json.dumps(json.loads(data), indent = 2)+'\n'
                s1 = data.splitlines(keepends=True)

            with open(filename) as fd:
                s2 = fd.read().splitlines(keepends=True)

            lines = unified_diff(
                s1,
                s2,
                fromfile=template,
                tofile=filename
            )

            # try:
                # first_line = next(lines)
                # sys.stdout.writelines(['diff\n', 'index\n', first_line])
            sys.stdout.writelines(lines)
            # except StopIteration:
                # pass
