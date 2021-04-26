
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(

    name='sak', version='0.5.0',

    description='Swiss Army Knife',
    long_description='sak is a module, submodule and function based tool',

    author='make-github-pseudonymous-again',
    author_email='aurelien.ooms@gmail.com',
    url='https://github.com/make-github-pseudonymous-again/sak',
    license='LICENSE',

    install_requires=[
        'lxml',
        'semantic_version'
    ],

    packages=[
        'sak',
        'sak.test',
        'lib',
        'lib.nice'
    ],

    scripts=['$']
)
