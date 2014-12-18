
try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

setup(
	name='sak',
	version='0.0.1',
	author='aureooms',
	author_email='aurelien.ooms@gmail.com',
	scripts=['sak'],
	url='https://github.com/aureooms/sake',
	license='LICENSE',
	description='Swiss Army KnifE',
	long_description=open('README').read(),
	install_requires=[
		"lxml",
		"semantic_version"
	],
)
