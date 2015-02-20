
import lib.args , os.path

@lib.args.convert( directory = os.path.abspath , port = int )
def lighttpd ( directory , port ) :

	config = """
server.modules = (
		"mod_access",
		"mod_alias",
		"mod_compress",
		"mod_redirect",
		"mod_auth",
		"mod_cgi"
)

cgi.assign      = ( ".cgi" => "" )

server.port                     = %d
server.document-root            = "%s"
server.errorlog                 = "/dev/stdout"
server.dir-listing              = "enable"
dir-listing.encoding            = "utf-8"
index-file.names                = ( "index.cgi", "index.html")
include_shell "/usr/share/lighttpd/create-mime.assign.pl"
"""

	print( config % ( port , directory ) )
