
import getpass, ftplib

class FTP(ftplib.FTP):

	def __init__(self, *args):
		ftplib.FTP.__init__(self, *args)
		self.FILE = '-'
		self.DIR = 'd'
		self.LINK = 'l'

	def storbinary(self, path, fd):
		super(FTP, self).storbinary('STOR %s' % path, fd)

	def chmod(self, mod, path):
		return self.sendcmd('SITE CHMOD %s %s' % (mod, path))

	def poke(self, path):
		if len(path) == 0 or path[0] != '/' : path = self.pwd() + '/' + path
		return (path, self.nlst(path))

	def isfile(self, path):
		path, l = self.poke(path)
		return len(l) == 1 and l[0] == path

	def isdir(self, path):
		path, l = self.poke(path)
		return len(l) > 0 and l[0] != path

	def ls(self, path = '.'):
		if path == '..' : path = '../'
		d = []
		self.retrlines('LIST %s' % path, lambda x : d.append((x[0], ''.join(x.split()[8:]))))
		return d

	def loginprompt(self, config):
		print(self.connect(config['host']))
		username = config['username'] if 'username' in config else input('Username for \'ftp://%s\' : ' % (config['host']))
		password = getpass.getpass('Password for \'ftp://%s@%s\' : ' % (username, config['host']))
		print(self.login(username, password))
		print(self.cwd(config['root']))
