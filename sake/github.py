import lib

def grab(what, user = None):

	if user is None : user = lib.config.prompt_user('github.com', 'github')

	lib.sys.call(['git', 'clone', 'https://%s@github.com/%s.git' % (user, what)], stdout = None, stderr = None)
