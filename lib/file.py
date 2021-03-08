
import hashlib
import lib.dir
import shutil
import os
import os.path


def read(f, callback, blocksize=2**15):
    chunk = f.read(blocksize)
    while len(chunk) > 0:
        callback(chunk)
        chunk = f.read(blocksize)


def hash(f, h=None, blocksize=2**15):
    if h is None:
        h = hashlib.sha256()
    read(f, h.update, blocksize)
    return h


def walk(src, f):

    def callback(path):
        with open(path, 'r') as g:
            f(g)

    lib.dir.walk(src, f=callback)

def iterall(*src,root='',exclude=frozenset()):
    # TODO improve using os.scandir
    for s in src :
        path = root + s
        if path in exclude :
            continue
        elif os.path.isdir(path):
            yield from iterall(*os.listdir(path),root=path+'/',exclude=exclude)
        elif os.path.isfile(path):
            yield path


def move(a, cwd):

    if not isinstance(a, (list)):
        a = [a]

    absolute = lambda path: os.path.join(cwd, path)

    for m in a:
        shutil.move(*map(absolute, m))


def rm(*paths, **kwargs):

    recursive = kwargs.get("recursive", False)
    force = kwargs.get("force", False)

    for path in paths:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)
        elif not force:
            raise Exception("path '%s' does not exist" % path)


def touch(*files, **kwargs):
    """
            http://stackoverflow.com/a/1160227/1582182
    """

    times = kwargs.get("times", None)

    for fname in files:

        with open(fname, 'a'):
            os.utime(fname, times)


def lineiterator(fp):

    return (line[:-1].decode() for line in iter(fp.readline, b""))
