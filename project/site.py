import json, os, base64, tempfile, hashlib, lib, socket


def down(directory = '.', config_file = 'json/config.json', dry_run = False):
	local = {'root' : os.path.abspath(directory)}

	pre = lambda *x: None

	def callback(ftp, helper, config):
		helper.server_down(ftp, config, local)

	_helper.wrap(local, config_file, dry_run, pre, callback)

def up(directory = '.', config_file = 'json/config.json', dry_run = False):
	local = {'root' : os.path.abspath(directory)}

	pre = lambda *x: None

	def callback(ftp, helper, config):
		helper.server_up(ftp, config, local)
		
	_helper.wrap(local, config_file, dry_run, pre, callback)


def diff(directory = '.', config_file = 'json/config.json'):
	return push(directory, config_file, dry_run = True)


def push(directory = '.', config_file = 'json/config.json', dry_run = False):

	local = {
		'root' : os.path.abspath(directory),
		'hash' : {},
		'tree' : {}
	}

	def pre(helper, config):
		helper.local_fetch(local['root'], config, local['hash'], local['tree'])

	def callback(ftp, helper, config):

		server = {
			'root' : config['root'],
			'hash' : {},
			'tree' : {}
		}

		helper.server_fetch(ftp, config, server)
		helper.update(ftp, config, local, server)

	_helper.wrap(local, config_file, dry_run, pre, callback)


def hash(config_file = 'json/config.json'):

	try:
		with open(config_file, 'r') as f : config = json.load(f)

	except FileNotFoundError as e:
		print(e)
		return

	helper = _helper(dry_run = False)

	with lib.ftp.FTP() as ftp:
		try:

			ftp.loginprompt(config)

			server = {
				'hash' : {},
				'tree' : {}
			}

			helper.server_hash(ftp, config, server['hash'], server['tree'])
			helper.send_hash(ftp, config, server)

		except socket.gaierror as e:
			print(e)




class _helper:

	def __init__(self, dry_run):
		self.do = not dry_run

	def wrap(local, config_file, dry_run, pre, callback):

		if not os.path.isdir(local['root']): print('[Errno 1] Local root \'%s\' not found' % local['root']); return

		try:
			with open(os.path.join(local['root'], config_file), 'r') as f : config = json.load(f)

		except FileNotFoundError as e:
			print(e)
			return

		helper = _helper(dry_run)

		pre(helper, config)

		with lib.ftp.FTP() as ftp:

			try:
				ftp.loginprompt(config)
				callback(ftp, helper, config)

			except socket.gaierror as e:
				print(e)

	def local_fetch(self, root, config, hash_t, tree_i, current = '', tree = None):
		if tree is None : tree = config['tree']
		dir_list = os.listdir(root + '/' + current)
		for item, what in tree.items():
			minipath = current + item
			path = root + '/' + minipath
			if os.path.isfile(path):
				base, ext = os.path.splitext(minipath)
				if ext == config['online'] :
					if os.path.basename(minipath) in tree : continue
					else : dest = base
				elif item + config['online'] in dir_list :
					dest = minipath
					path += config['online']
					minipath += config['online']
				else : dest = minipath
				with open(path, 'rb') as f : h = lib.file.hash(f).digest()
				h_ascii = base64.b64encode(h).decode('ascii')
				hash_t.setdefault(h_ascii, {'s' : [], 'd' : []})
				hash_t[h_ascii]['s'].append(minipath)
				hash_t[h_ascii]['d'].append(dest)
				tree_i[item] = [h_ascii, dest]

			elif os.path.isdir(path):
				if what is None : what = { sub : None for sub in os.listdir(path)}
				tree_i[item] = {}
				self.local_fetch(root, config, hash_t, tree_i[item], current + item + '/', what)


	def server_fetch(self, ftp, config, server):
		index_file = '/%s/%s' % (config['root'], config['index'])
		if ftp.isfile(index_file):
			chuncks = []
			ftp.retrlines('RETR %s' % index_file, chuncks.append)
			index = ''.join(chuncks)
			data = json.loads(index)
			server['hash'] = data['hash']
			server['tree'] = data['tree']


	def ensure_structure_rec(self, ftp, config, local_h, current):
		for item, data in local_h.items():
			if type(data) == dict:
				print('ftp.mkd(\'/%s/%s%s\')' % (config['root'], current, item))
				if self.do : ftp.mkd('/%s/%s%s' % (config['root'], current, item))
				self.ensure_structure_rec(ftp, config, local_h[item], current + item + '/')

	def ensure_structure(self, ftp, config, local_h, server_h, current = ''):

		for item, data in local_h.items():
			if type(data) == dict:
				if item not in server_h:
					print('ftp.mkd(\'/%s/%s%s\')' % (config['root'], current, item))
					if self.do : ftp.mkd('/%s/%s%s' % (config['root'], current, item))
					self.ensure_structure_rec(ftp, config, local_h[item], current + item + '/')
				else:
					self.ensure_structure(ftp, config, local_h[item], server_h[item], current + item + '/')


	def clean_structure(self, ftp, config, local_h, server_h, current = ''):

		for item, data in server_h.items():
			if type(data) == dict:
				if item not in local_h:
					print('ftp.rmd(\'/%s/%s%s\')' % (config['root'], current, item))
					if self.do : ftp.rmd('/%s/%s%s' % (config['root'], current, item))
				else:	
					self.clean_structure(ftp, config, local_h[item], server_h[item], current + item + '/')

	def update_deleted_moved_copied(self, ftp, config, local, server):
		for h, minipaths in server['hash'].items():

			# deleted files
			if h not in local['hash']:
				for i in range(len(minipaths)):
					print('ftp.delete(\'/%s/%s\')' % (config['root'], minipaths[i]))
					if self.do : ftp.delete('/%s/%s' % (config['root'], minipaths[i]))

			else:

				not_handled = local['hash'][h]['d'].copy()

				for i in range(len(minipaths)):
					minipath = minipaths[i]

					# moved files
					if minipath not in local['hash'][h]['d']:
						if len(not_handled) > 0:
							for j in range(len(not_handled)):
								if not_handled[j] not in minipaths:
									replace = not_handled[j]
									del not_handled[j]
									break

							print('ftp.rename(\'/%s/%s\', \'/%s/%s\')' % (config['root'], minipath, config['root'], replace))
							if self.do : ftp.rename('/%s/%s' % (config['root'], minipath), '/%s/%s' % (config['root'], replace))
						else:
							print('ftp.delete(\'/%s/%s\')' % (config['root'], minipath))
							if self.do : ftp.delete('/%s/%s' % (config['root'], minipath))

					# not moved
					else:
						not_handled.remove(minipath)

				# copied files
				if len(not_handled) > 0:
					base = local['hash'][h]['s'][0]
					with open('%s/%s' % (local['root'], base), 'rb') as f:
						for i in range(len(not_handled)):
							f.seek(0)
							print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], not_handled[i], f))
							if self.do : ftp.storbinary('STOR /%s/%s' % (config['root'], not_handled[i]), f)


	def update_added(self, ftp, config, local, server):
		for h, paths in local['hash'].items():
			# added files
			if h not in server['hash']:
				for i in range(len(paths['s'])):
					with open('%s/%s' % (local['root'], paths['s'][i]), 'rb') as f:
						print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], paths['d'][i], f))
						if self.do : ftp.storbinary('STOR /%s/%s' % (config['root'], paths['d'][i]), f)

	def update_modified(self, ftp, config, local_h, server_h, current = ''):

		for item, data in local_h.items():
			# modified files
			if type(data) == list:
				h, dest = data
				if dest in server_h and h != server_h[dest]:
					with open('%s/%s%s' % (local['root'], current, item), 'rb') as f:
						print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], current, dest, f))
						if self.do : ftp.storbinary('STOR /%s/%s' % (config['root'], minipath), f)


			elif item in server_h:
				self.update_modified(ftp, config, data, server_h[item], current + item + '/')


	def update_index(self, ftp, config, local):
		data = {
			'hash' : {},
			'tree' : {}
		}

		for key in local['hash']:
			data['hash'][key] = local['hash'][key]['d']

		def rec_build(local_t, server_t):
			for item, value in local_t.items():
				if type(value) == list:
					server_t[item] = value[0]
				elif type(value) == dict:
					server_t[item] = {}
					rec_build(value, server_t[item])

		rec_build(local['tree'], data['tree'])


		with open('%s/%s' % (local['root'], config['index']), 'w') as f:
			json.dump(data, f, indent = '\t')

		with open('%s/%s' % (local['root'], config['index']), 'rb') as f:
			print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], config['index'], f))
			if self.do : ftp.storbinary('STOR /%s/%s' % (config['root'], config['index']), f)
			print('ftp.chmod(\'640\', \'/%s/%s\')' % (config['root'], config['index']))
			if self.do : ftp.chmod('640', '/%s/%s' % (config['root'], config['index']))

	def update(self, ftp, config, local, server):
		self.ensure_structure(ftp, config, local['tree'], server['tree'])
		self.update_deleted_moved_copied(ftp, config, local, server)
		self.update_added(ftp, config, local, server)
		# self.update_modified(ftp, config, local['tree'], server['tree'])
		self.update_index(ftp, config, local)
		self.clean_structure(ftp, config, local['tree'], server['tree'])



	def server_hash(self, ftp, config, hash_t, tree, current = ''):
		for t, item in ftp.ls(current):
			print('%s%s' % (current, item))
			if item == '.' or item == '..' or item == config['index'] : continue
			minipath = current + item
			path = '/' + config['root'] + '/' + minipath
			if t == ftp.FILE:
				hasher = hashlib.sha256()
				ftp.retrbinary('RETR /%s/%s' % (config['root'], minipath), hasher.update)
				h = hasher.digest()
				h_ascii = base64.b64encode(h).decode('ascii')
				print(h_ascii)
				hash_t.setdefault(h_ascii, [])
				hash_t[h_ascii].append(minipath)
				tree[item] = h_ascii

			elif t == ftp.DIR:
				tree[item] = {}
				self.server_hash(ftp, config, hash_t, tree[item], current + item + '/')

	def send_hash(self, ftp, config, data):
		with tempfile.NamedTemporaryFile('w', delete = False) as tmp:
			json.dump(data, tmp, indent = '\t')

		with open(tmp.name, 'rb') as f:
			print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], config['index'], f))
			if self.do : ftp.storbinary('STOR /%s/%s' % (config['root'], config['index']), f)

		os.remove(tmp.name)

		print('ftp.chmod(\'640\', \'/%s/%s\')' % (config['root'], config['index']))
		if self.do : ftp.chmod('640', '/%s/%s' % (config['root'], config['index']))



	def server_down(self, ftp, config, local):
		return self.server_switch(ftp, config, local, 'down')



	def server_up(self, ftp, config, local):
		return self.server_switch(ftp, config, local, 'up')


	def server_switch(self, ftp, config, local, which):
		src = os.path.join(local['root'], config[which])
		if os.path.isfile('%s%s' % (src, config['online'])) : src += config['online']

		with open(src, 'rb') as f:
			print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], config['up'], f))
			if self.do : ftp.storbinary('STOR /%s/%s' % (config['root'], config['up']), f)

