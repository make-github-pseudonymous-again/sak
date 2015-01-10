import lib

def refresh(user, repo):

	lib.sys.call([
		'curl',
		'--data',
		'',
		'https://codeclimate.com/github/%s/%s/refresh' % (user, repo)
	])
