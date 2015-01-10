import lib.git

def vimbundle ( url ) :

	repo = url.split("/")[-1]

	lib.git.submodule( "add" , url, ".vim/bundle/%s" % repo )
