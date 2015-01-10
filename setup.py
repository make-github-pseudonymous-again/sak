
try : from setuptools import setup
except ImportError : from distutils.core import setup

setup (

	name = 'sak' , version = '0.0.2' ,

	description = 'Swiss Army KnifE',
	long_description = open( 'README.md' ).read( ) ,

	author = 'aureooms' ,
	author_email = 'aurelien.ooms@gmail.com' ,
	url = 'https://github.com/aureooms/sak' ,
	license = 'LICENSE' ,

	install_requires = [
		'lxml' ,
		'semantic_version'
	] ,

	packages = [
		'sak' ,
		'lib' ,
		'lib.nice'
	] ,

	scripts = [ '$' ]
)
