import lib.config, lib.git

DOMAIN = 'bitbucket.org'

def clone(what, user = None):

	if user is None : user = lib.config.prompt_user(DOMAIN, 'bitbucket')

	lib.git.clone('https://%s@%s/%s.git' % (user, DOMAIN, what))
