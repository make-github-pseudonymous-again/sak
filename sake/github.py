import lib.config, lib.git

DOMAIN = 'github.com'

def clone(what, user = None):

	if user is None : user = lib.config.prompt_user(DOMAIN, 'github')

	lib.git.clone('https://%s@%s/%s.git' % (user, DOMAIN, what))
