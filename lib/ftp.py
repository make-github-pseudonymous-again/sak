import getpass

class wrap:

	def __init__(self, ftp):
		self.ftp = ftp

		self.FILE = '-'
		self.DIR = 'd'
		self.LINK = 'l'

	def chmod(self, mod, path):
		return self.ftp.sendcmd('SITE CHMOD %s %s' % (mod, path))

	def isfile(self, path):
		if len(path) == 0 or path[0] != '/' : path = self.ftp.pwd() + '/' + path
		l = self.ftp.nlst(path)
		return len(l) == 1 and l[0] == path

	def isdir(self, path):
		if len(path) == 0 or path[0] != '/' : path = self.ftp.pwd() + '/' + path
		l = self.ftp.nlst(path)
		return len(l) > 0 and l[0] != path

	def ls(self, path = '.'):
		if path == '..' : path = '../'
		d = []
		self.ftp.retrlines('LIST %s' % path, lambda x : d.append((x[0], ''.join(x.split()[8:]))))
		return d



	def loginprompt(self, config):
		print(self.ftp.connect(config['host']))
		username = config['username'] if 'username' in config else input('Username for \'ftp://%s\' : ' % (config['host']))
		password = getpass.getpass('Password for \'ftp://%s@%s\' : ' % (username, config['host']))
		print(self.ftp.login(username, password))
		print(self.ftp.cwd(config['root']))


	def connect(self, *args):
		return self.ftp.connect(*args)

	def login(self, *args):
		return self.ftp.login(*args)

	def voidcmd(self, *args):
		return self.ftp.voidcmd(*args)

	def sendcmd(self, *args):
		return self.ftp.sendcmd(*args)

	def rename(self, *args):
		return self.ftp.rename(*args)

	def delete(self, *args):
		return self.ftp.delete(*args)

	def mkd(self, *args):
		return self.ftp.mkd(*args)

	def rmd(self, *args):
		return self.ftp.rmd(*args)

	def cwd(self, *args):
		return self.ftp.cwd(*args)

	def retrlines(self, *args):
		return self.ftp.retrlines(*args)

	def retrbinary(self, *args):
		return self.ftp.retrbinary(*args)

	def nlst(self, *args):
		return self.ftp.nlst(*args)

	def storbinary(self, *args):
		return self.ftp.storbinary(*args)

	def storlines(self, *args):
		return self.ftp.storlines(*args)

	def quit(self, *args):
		return self.ftp.quit(*args)

	def close(self, *args):
		return self.ftp.close(*args)

	def size(self, *args):
		return self.ftp.size(*args)

	def pwd(self, *args):
		return self.ftp.size(*args)

	def dir(self, *args):
		return self.ftp.dir(*args)