import hashlib, base64, tempfile, lib.json, os


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


	def hash(self, root, htree, tree, skip, current = ''):
		for t, item in self.ftp.ls(current):

			if item == '.' or item == '..' or skip(current, item) : continue

			minipath = current + item

			if t == self.ftp.FILE:
				digest = self.hascii('/%s/%s' % (root, minipath))
				print('%s > %s' % (minipath, digest))

				htree.setdefault(digest, [])
				htree[digest].append(minipath)
				tree[item] = digest

			elif t == self.ftp.DIR:
				tree[item] = {}
				self.hash(root, htree, tree[item], skip, current + item + '/')


	def _makedirs(self, root, model, current):
		for item, data in model.items():
			if type(data) == dict:
				self.mkd('/%s/%s%s' % (root, current, item))
				self._makedirs(root, model[item], current + item + '/')

	def makedirs(self, root, model, actual, current = ''):

		for item, data in model.items():
			if type(data) == dict:
				if item not in actual:
					self.mkd('/%s/%s%s' % (root, current, item))
					self._makedirs(root, model[item], current + item + '/')
				else:
					self.makedirs(root, model[item], actual[item], current + item + '/')


	def _removedirs(self, root, subtree, current):
		for item, data in subtree.items():
			if type(data) == dict : self._removedirs(root, data, current + '/' + item)

		self.rmd('/%s/%s' % (root, current))


	def removedirs(self, root, model, actual, current = ''):

		for item, entry in actual.items():
			if type(entry) == dict:
				if item not in model:
					self._removedirs(root, entry, current + item)
				else:	
					self.removedirs(root, model[item], entry, current + item + '/')


	def sendJSON(self, path, data):
		with tempfile.NamedTemporaryFile('w', delete = False) as tmp:
			lib.json.pretty(data, tmp)

		with open(tmp.name, 'rb') as fd : self.storbinary(path, fd)

		os.remove(tmp.name)