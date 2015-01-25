
def human ( size ) :

	"""

		>>> from lib.bytes import *
		>>> human( 23 )
		'23.000000 B'
		>>> human( 1024 )
		'1.000000 KB'
		>>> human( 1025 )
		'1.000977 KB'
		>>> human( 1024 ** 4 )
		'1.000000 TB'
		>>> human( 1024 ** 5 )
		'1024.000000 TB'

	"""

	radix = 1024.
	units = ["B", "KB", "MB", "GB", "TB"]
	last = units[-1]

	for u in units :
		if u == last or size < radix : break
		size /= radix

	return "%f %s" % ( size , u )
