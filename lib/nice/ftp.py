import hashlib


class FTP(object):


	def __init__(self, ftp, do):
		self.ftp = ftp
		self.do = do


	def chmod(self, mode, path):
		print("ftp.chmod('%s', '%s')" % (mode, path))
		if self.do : self.ftp.chmod(mode, path)

	def storbinary(self, path, fd):
		print("ftp.storbinary('STOR %s', %s)" % (path, fd))
		if self.do : self.ftp.storbinary('STOR %s' % path, fd)

	def mkd(self, path):
		print("ftp.mkd('%s')" % path)
		if self.do : self.ftp.mkd(path)

	def rmd(self, path):
		print("ftp.rmd('%s')" % path)
		if self.do : self.ftp.rmd(path)

	def delete(self, path):
		print("ftp.delete('%s')" % path)
		if self.do : self.ftp.delete(path)

	def rename(self, fr, to):
		print("ftp.rename('%s', '%s')" % (fr, to))
		if self.do : self.ftp.rename('%s' % fr, '%s' % to)

	def hascii(self, path):
		hasher = hashlib.sha256()
		self.ftp.retrbinary('RETR %s' % path, hasher.update)
		h = hasher.digest()
		return base64.b64encode(h).decode('ascii')