
import subprocess

IGNORE = '.gitignore'


def do(action, *args, check=True, **kwargs):
    return subprocess.run(['git', action] + list(args), check=check, **kwargs)


def clone(*args, **kwargs):
    return do('clone', *args, **kwargs)


def pull(*args, **kwargs):
    return do('pull', *args, **kwargs)


def push(*args, **kwargs):
    return do('push', *args, **kwargs)


def commit(*args, **kwargs):
    return do('commit', *args, **kwargs)


def remote(*args, **kwargs):
    return do('remote', *args, **kwargs)


def add(*args, **kwargs):
    return do('add', *args, **kwargs)


def status(*args, **kwargs):
    return do('status', *args, **kwargs)


def diff(*args, **kwargs):
    return do('diff', *args, **kwargs)


def tag(*args, **kwargs):
    return do('tag', *args, **kwargs)


def log(*args, **kwargs):
    return do('log', *args, **kwargs)


def checkout(*args, **kwargs):
    return do('checkout', *args, **kwargs)

def branch(*args, **kwargs):
    return do('branch', *args, **kwargs)

def submodule(*args, **kwargs):
    return do('submodule', *args, **kwargs)
