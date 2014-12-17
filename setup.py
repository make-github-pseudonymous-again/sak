
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
	name='Sake',
	version='0.0.1',
	author='aureooms',
	author_email='aurelien.ooms@gmail.com',
	packages=['sak'],
	scripts=['main.py'],
	url='http://pypi.python.org/pypi/TowelStuff/',
	license='LICENSE',
	description='Swiss Army KnifE',
	long_description=open('README.md').read(),
	install_requires=[
		"lxml",
		"semantic_version"
	],
)
