# requires https://github.com/bevry/cson

import os, tempfile, json, lib.sys


def load ( fp ) :

	return loads( fp.read() )


def loads ( string ) :

	with tempfile.NamedTemporaryFile( "w", delete = False, suffix = ".cson" ) as tmp :

		tmp.write( string )

	out, err, p = lib.sys.call( ["cson2json", tmp.name] )

	os.remove( tmp.name )

	return json.loads( out.decode() )


def dump ( obj, fp ) :

	fp.write( dumps( obj ) )


def dumps ( obj ) :

	with tempfile.NamedTemporaryFile( "w", delete = False, suffix = ".json" ) as tmp :

		json.dump( obj, tmp )

	out, err, p = lib.sys.call( ["json2cson", tmp.name] )

	os.remove( tmp.name )

	return out.decode()
