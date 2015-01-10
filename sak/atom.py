import os, lib.cson, sak.cat, itertools, lib.atom

PROJECTSFILE = os.path.expanduser( "~/.atom/projects.cson" )


def project ( directory ) :

	print( lib.atom.project( directory ) )


def projects () :

	sak.cat.text( PROJECTSFILE )


def add ( directory = ".", *others ) :

	with open( PROJECTSFILE ) as f :
		projects = lib.cson.load( f )


	for target in itertools.chain( [directory], others ) :

		path, name = lib.atom.project( target )

		projects[name] = dict( title = name, paths = [path] )


	with open( PROJECTSFILE, "w" ) as f :
		lib.cson.dump( projects, f )



def remove ( directory = ".", *others ) :

	with open( PROJECTSFILE ) as f :
		projects = lib.cson.load( f )


	for target in itertools.chain( [directory], others ) :

		path, name = lib.atom.project( target )

		if name in projects :
			del projects[name]


	with open( PROJECTSFILE, "w" ) as f :
		lib.cson.dump( projects, f )
