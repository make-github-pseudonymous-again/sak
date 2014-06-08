import lib, subprocess

def grab(what, user = None):

	if user is None : user = lib.config.prompt_user('bitbucket.org', 'bitbucket')

	lib.sys.call(['git', 'clone', 'https://%s@bitbucket.org/%s.git' % (user, what)], stdout = None, stderr = None)
