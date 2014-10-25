from __future__ import absolute_import, division, print_function, unicode_literals

import os, lib.cson, sake.cat

PROJECTSFILE = os.path.expanduser( "~/.atom/projects.cson" )


def project( directory ) :

	path = os.path.abspath( directory )
	name = os.path.basename( path )

	return path, name


def projects() :

	sake.cat.text( PROJECTSFILE )


def add( directory = ".", *others ) :

	path, name = project( directory )

	with open( PROJECTSFILE ) as f :
		projects = lib.cson.load( f )

	projects[name] = dict( title = name, paths = [path] )

	with open( PROJECTSFILE, "w" ) as f :
		lib.cson.dump( projects, f )

	if others : add( *others )


def remove( directory = ".", *others ) :

	path, name = project( directory )

	with open( PROJECTSFILE ) as f :
		projects = lib.cson.load( f )

	if name in projects :
		del projects[name]

	with open( PROJECTSFILE, "w" ) as f :
		lib.cson.dump( projects, f )

	if others : remove( *others )
