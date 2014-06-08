import os, json, socket, tempfile, lib.ftp, lib.nice.ftp, lib.nice.file



class FTPSite(object):

	default = {
		"host" : "hostaddr",
		"username" : "username",
		"root"   : "www",

		"index"  : ".hash",
		"online" : ".online",

		"down"   : ".htaccess",
		"up"     : ".htaccess",
		
		"tree"   : {},
		"ignore" : []
	}

	def __init__(self, dry_run):
		self.do = not dry_run
		self.ftp = None
		self.remote = None

	def setFTP(self, ftp):
		self.ftp = ftp
		self.remote = lib.nice.ftp.FTP(ftp, self.do)

	def check_local_root(root):
		if not os.path.isdir(root):
			print("[Errno 1] Local root '%s' not found" % root)
			return False

		else:
			return True

	def wrap(local, config_file, dry_run, pre, callback):

		try:
			config = FTPSite.default.copy()
			with open(os.path.join(local['root'], config_file), 'r') as f:
				config.update(json.load(f))

		except FileNotFoundError as e:
			print(e)
			return

		helper = FTPSite(dry_run)

		pre(helper, config)

		with lib.ftp.FTP() as ftp:
			helper.setFTP(ftp)

			try:
				ftp.loginprompt(config)
				callback(helper, config)

			except socket.gaierror as e:
				print(e)



	def local_file(self, config, hash_t, tree_i, tree, dir_list, item, minipath, path):
		base, ext = os.path.splitext(minipath)
		if ext == config['online'] :
			if os.path.basename(minipath) in tree : return
			else : dest = base
		elif item + config['online'] in dir_list :
			dest = minipath
			path += config['online']
			minipath += config['online']
		else : dest = minipath
		h_ascii = lib.nice.file.hascii(path)
		hash_t.setdefault(h_ascii, {'s' : [], 'd' : []})
		hash_t[h_ascii]['s'].append(minipath)
		hash_t[h_ascii]['d'].append(dest)
		tree_i[item] = [h_ascii, dest]

	def local_fetch(self, root, config, hash_t, tree_i, current = '', tree = None):
		if tree is None : tree = config['tree']
		dir_list = os.listdir(root + '/' + current)
		for item, what in tree.items():
			minipath = current + item
			path = root + '/' + minipath
			if os.path.isfile(path):
				self.local_file(config, hash_t, tree_i, tree, dir_list, item, minipath, path)

			elif os.path.isdir(path):
				if what is None : what = { sub : None for sub in os.listdir(path)}
				tree_i[item] = {}
				self.local_fetch(root, config, hash_t, tree_i[item], current + item + '/', what)


	def server_fetch(self, config, server):
		index_file = '/%s/%s' % (config['root'], config['index'])
		if self.ftp.isfile(index_file):
			chuncks = []
			self.ftp.retrlines('RETR %s' % index_file, chuncks.append)
			index = ''.join(chuncks)
			data = json.loads(index)
			server['hash'] = data['hash']
			server['tree'] = data['tree']




	def delete_minipaths(self, minipaths, root):
		for minipath in minipaths:
			self.remote.delete('/%s/%s' % (root, minipath))


	def update_moved(self, config, local, h, not_handled, minipaths):	
		for minipath in minipaths:

			# moved files
			if minipath not in local['hash'][h]['d']:
				if len(not_handled) > 0:
					replace = not_handled[0]
					del not_handled[0]

					self.remote.rename('/%s/%s' % (config['root'], minipath), '/%s/%s' % (config['root'], replace))
				else:
					self.remote.delete('/%s/%s' % (config['root'], minipath))

			# not moved
			else:
				pass

	def update_copied(self, config, local, h, not_handled):
		base = local['hash'][h]['s'][0]
		with open('%s/%s' % (local['root'], base), 'rb') as f:
			for i in range(len(not_handled)):
				f.seek(0)
				self.remote.storbinary('/%s/%s' % (config['root'], not_handled[i]), f)

	def update_moved_copied_minipaths(self, config, local, h, minipaths):
		not_handled = [x for x in local['hash'][h]['d'] if x not in minipaths]

		self.update_moved(config, local, h, not_handled, minipaths)

		if len(not_handled) > 0 : self.update_copied(config, local, h, not_handled)
		

	def update_deleted_moved_copied(self, config, local, server):
		for h, minipaths in server['hash'].items():

			# deleted files
			if h not in local['hash']:
				self.delete_minipaths(minipaths, config['root'])

			else:
				self.update_moved_copied_minipaths(config, local, h, minipaths)

	def add_paths(self, config, local, paths):
		for i in range(len(paths['s'])):
			with open('%s/%s' % (local['root'], paths['s'][i]), 'rb') as f:
				self.remote.storbinary('/%s/%s' % (config['root'], paths['d'][i]), f)

	def update_added(self, config, local, server):
		for h, paths in local['hash'].items():
			# added files
			if h not in server['hash']:
				self.add_paths(config, local, paths)




	def rec_build(local_t, server_t):
		for item, value in local_t.items():
			if type(value) == list:
				server_t[item] = value[0]
			elif type(value) == dict:
				server_t[item] = {}
				FTPSite.rec_build(value, server_t[item])

	def update_index(self, config, local):
		data = {
			'hash' : {},
			'tree' : {}
		}

		for key in local['hash']:
			data['hash'][key] = local['hash'][key]['d']


		FTPSite.rec_build(local['tree'], data['tree'])


		with open('%s/%s' % (local['root'], config['index']), 'w') as f:
			json.dump(data, f, indent = '\t')

		with open('%s/%s' % (local['root'], config['index']), 'rb') as f:
			self.remote.storbinary('/%s/%s' % (config['root'], config['index']), f)
			self.remote.chmod('640', '/%s/%s' % (config['root'], config['index']))

	def update(self, config, local, server):
		self.remote.makedirs(config['root'], local['tree'], server['tree'])
		self.update_deleted_moved_copied(config, local, server)
		self.update_added(config, local, server)
		self.update_index(config, local)
		self.remote.removedirs(config['root'], local['tree'], server['tree'])


	def server_hash(self, config, htree, tree, current = ''):
		isindex = lambda item : item == config['index']
		ignored = lambda path : path in config['ignore']
		skip = lambda current, item :  isindex(item) or ignored(current + item)
		self.remote.hash(config['root'], htree, tree, skip, current)


	def send_hash(self, config, data):
		path = '/%s/%s' % (config['root'], config['index'])
		self.remote.sendJSON(path, data)
		self.remote.chmod('640', path)



	def server_down(self, config, local):
		return self.server_switch(config, local, 'down')



	def server_up(self, config, local):
		return self.server_switch(config, local, 'up')


	def server_switch(self, config, local, which):
		src = os.path.join(local['root'], config[which])
		if os.path.isfile('%s%s' % (src, config['online'])) : src += config['online']

		with open(src, 'rb') as f:
			self.remote.storbinary('/%s/%s' % (config['root'], config['up']), f)

