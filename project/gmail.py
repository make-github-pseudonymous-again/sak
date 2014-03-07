import sys, getpass, urllib.parse, urllib.request as urllib2, lib

def get(user = None, passwd = None):

	if user is None : user, passwd = lib.config.module('gmail')
	if passwd is None : passwd = lib.config.user('user')

	url = 'https://%smail.google.com'
	if user is None : user = input('Username for \'%s\' : ' % url % '')
	url = url % (urllib.parse.quote_plus(user).replace('%', '%%') + '%s@')
	if passwd is None : passwd = getpass.getpass('Password for \'%s\' : ' % url % '')


	auth_handler = urllib2.HTTPBasicAuthHandler()
	auth_handler.add_password(
		realm = 'New mail feed',
		uri = 'https://mail.google.com',
		user = user,
		passwd = passwd
	)

	opener = urllib2.build_opener(auth_handler)
	feed = opener.open('https://mail.google.com/mail/feed/atom')

	contents = feed.read().decode('utf-8')

	i = contents.index('<fullcount>') + 11
	j = contents.index('</fullcount>')

	unread = contents[i:j]

	print(unread)