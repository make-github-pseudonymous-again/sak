import hashlib, base64, tempfile, lib.json, os


class FTP(object):


	def __init__(self, ftp, do):
		self.ftp = ftp
		self.do = do

	def action(self, method, msg, args):
		print(msg % args)
		if self.do : method(*args)

	def chmod(self, mode, path):
		self.action(self.ftp.chmod, "ftp.chmod('%s', '%s')", (mode, path))

	def storbinary(self, path, fd):
		self.action(self.ftp.storbinary, "ftp.storbinary('STOR %s', %s)", (path, fd))

	def mkd(self, path):
		self.action(self.ftp.mkd, "ftp.mkd('%s')", (path,))

	def rmd(self, path):
		self.action(self.ftp.rmd, "ftp.rmd('%s')", (path,))

	def delete(self, path):
		self.action(self.ftp.delete, "ftp.delete('%s')", (path,))

	def rename(self, fr, to):
		self.action(self.ftp.rename, "ftp.rename('%s', '%s')", (fr, to))

	def hascii(self, path):
		hasher = hashlib.sha256()
		self.ftp.retrbinary('RETR %s' % path, hasher.update)
		h = hasher.digest()
		return base64.b64encode(h).decode('ascii')


	def ls( self , path ) :

		for itemtype , item in self.ftp.ls( path ) :

			if item != '.' and item != '..' :

				yield itemtype , item


	def hash(self, root, htree, tree, skip, current = ''):

		for t , item in self.ls( current ) :

			if skip( current , item ) :

				continue

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


	def recursivermd( self , path ) :

		for itemtype , item in self.ls( path ):

			itempath = path + '/' + item

			if itemtype == self.ftp.FILE:
				self.delete( itempath )

			elif itemtype == self.ftp.DIR:
				self.recursivermd( itempath )

		self.rmd( path )


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
