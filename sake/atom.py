# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os, lib.cson, sake.cat, itertools

PROJECTSFILE = os.path.expanduser( "~/.atom/projects.cson" )


def project( directory ) :

	path = os.path.abspath( directory )
	name = os.path.basename( path )

	return path, name


def projects() :

	sake.cat.text( PROJECTSFILE )


def add( directory = ".", *others ) :

	with open( PROJECTSFILE ) as f :
		projects = lib.cson.load( f )


	for target in itertools.chain( [directory], others ) :

		path, name = project( target )

		projects[name] = dict( title = name, paths = [path] )


	with open( PROJECTSFILE, "w" ) as f :
		lib.cson.dump( projects, f )



def remove( directory = ".", *others ) :

	with open( PROJECTSFILE ) as f :
		projects = lib.cson.load( f )


	for target in itertools.chain( [directory], others ) :

		path, name = project( target )

		if name in projects :
			del projects[name]


	with open( PROJECTSFILE, "w" ) as f :
		lib.cson.dump( projects, f )
