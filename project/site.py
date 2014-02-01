import ftplib, project.file, json, os, base64, tempfile, hashlib, lib.ftp


def diff(*args):
	return up(*args, dry_run = True)


def up(directory, config_file, dry_run = False):

	local = {
		'root' : os.path.abspath(directory),
		'checksum_table' : {},
		'hierarchy_tree' : {}
	}

	# fetch the config file to upload
	with open(config_file, 'r') as f : config = json.load(f)

	helper = __helper(dry_run)

	# build the local tree and table
	helper.local_fetch(local['root'], config, local['checksum_table'], local['hierarchy_tree'])

	# print(json.dumps(local['checksum_table'], indent = '\t'))
	# print(json.dumps(local['hierarchy_tree'], indent = '\t'))

	try:

		ftp = lib.ftp.wrap(ftplib.FTP())
		ftp.loginprompt(config)

		server = {
			'root' : config['root'],
			'checksum_table' : {},
			'hierarchy_tree' : {}
		}

		# fetch the server tree and table
		helper.server_fetch(ftp, config, server)

		# try to patch server by analyzing (diff local server)
		helper.update(ftp, config, local, server)

	# except ftplib.all_errors as e:
	# 	print('Socket error : %s' % (e))

	finally:
		ftp.quit()


def hash(config_file):

	# fetch the config file to upload
	with open(config_file, 'r') as f:
		config = json.load(f)

	helper = __helper(dry_run = False)

	try:

		ftp = lib.ftp.wrap(ftplib.FTP())
		ftp.loginprompt(config)

		server = {
			'checksum_table' : {},
			'hierarchy_tree' : {}
		}

		# build the server tree and table
		helper.server_hash(ftp, config, server['checksum_table'], server['hierarchy_tree'])

		# send it
		helper.send_hash(ftp, config, server)

	# except ftplib.all_errors as e:
	# 	print('Socket error : %s' % (e))

	finally:
		ftp.quit()



class __helper:

	def __init__(self, dry_run):
		self.do = not dry_run

	def local_fetch(self, root, config, checksum_table, hierarchy_tree, current = '', tree = None):
		if tree == None : tree = config['tree']
		dir_list = os.listdir(root + '/' + current)
		for item, what in tree.items():
			minipath = current + item
			path = root + '/' + minipath
			if os.path.isfile(path):
				base, ext = os.path.splitext(minipath)
				if ext == config['online_ext'] :
					if os.path.basename(minipath) in tree : continue
					else : dest = base
				elif item + config['online_ext'] in dir_list :
					dest = minipath
					path += config['online_ext']
					minipath += config['online_ext']
				else : dest = minipath
				with open(path, 'rb') as f:
					checksum = project.file.checksum(f).digest()
				checksum_ascii = base64.b64encode(checksum).decode('ascii')
				checksum_table.setdefault(checksum_ascii, {'s' : [], 'd' : []})
				checksum_table[checksum_ascii]['s'].append(minipath)
				checksum_table[checksum_ascii]['d'].append(dest)
				hierarchy_tree[item] = [checksum_ascii, dest]

			elif os.path.isdir(path):
				if what == None : what = { sub : None for sub in os.listdir(path)}
				hierarchy_tree[item] = {}
				self.local_fetch(root, config, checksum_table, hierarchy_tree[item], current + item + '/', what)


	def server_fetch(self, ftp, config, server):
		checksum_file = '/%s/%s' % (config['root'], config['checksum'])
		if ftp.isfile(checksum_file):
			chuncks = []
			ftp.retrlines('RETR %s' % checksum_file, chuncks.append)
			checksum = ''.join(chuncks)
			data = json.loads(checksum)
			server['checksum_table'] = data['checksum_table']
			server['hierarchy_tree'] = data['hierarchy_tree']

		# print(json.dumps(server['checksum_table'], indent = '\t'))
		# print(json.dumps(server['hierarchy_tree'], indent = '\t'))


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
		for checksum, minipaths in server['checksum_table'].items():

			# deleted files
			if checksum not in local['checksum_table']:
				for i in range(len(minipaths)):
					print('ftp.delete(\'/%s/%s\')' % (config['root'], minipaths[i]))
					if self.do : ftp.delete('/%s/%s' % (config['root'], minipaths[i]))

			else:

				not_handled = local['checksum_table'][checksum]['d'].copy()

				for i in range(len(minipaths)):
					minipath = minipaths[i]

					# moved files
					if minipath not in local['checksum_table'][checksum]['d']:
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
					base = local['checksum_table'][checksum]['s'][0]
					with open('%s/%s' % (local['root'], base), 'rb') as f:
						for i in range(len(not_handled)):
							f.seek(0)
							print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], not_handled[i], f))
							if self.do : ftp.storbinary('STOR /%s/%s' % (config['root'], not_handled[i]), f)


	def update_added(self, ftp, config, local, server):
		for checksum, paths in local['checksum_table'].items():
			# added files
			if checksum not in server['checksum_table']:
				for i in range(len(paths['s'])):
					with open('%s/%s' % (local['root'], paths['s'][i]), 'rb') as f:
						print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], paths['d'][i], f))
						if self.do : ftp.storbinary('STOR /%s/%s' % (config['root'], paths['d'][i]), f)

	def update_modified(self, ftp, config, local_h, server_h, current = ''):

		for item, data in local_h.items():
			# modified files
			if type(data) == list:
				checksum, dest = data
				if dest in server_h and checksum != server_h[dest]:
					with open('%s/%s%s' % (local['root'], current, item), 'rb') as f:
						print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], current, dest, f))
						if self.do : ftp.storbinary('STOR /%s/%s' % (config['root'], minipath), f)


			elif item in server_h:
				self.update_modified(ftp, config, data, server_h[item], current + item + '/')


	def update_checksum(self, ftp, config, local):
		data = {
			'checksum_table' : {},
			'hierarchy_tree' : {}
		}

		for key in local['checksum_table']:
			data['checksum_table'][key] = local['checksum_table'][key]['d']

		def rec_build(local_t, server_t):
			for item, value in local_t.items():
				if type(value) == list:
					server_t[item] = value[0]
				elif type(value) == dict:
					server_t[item] = {}
					rec_build(value, server_t[item])

		rec_build(local['hierarchy_tree'], data['hierarchy_tree'])


		with open('%s/%s' % (local['root'], config['checksum']), 'w') as f:
			json.dump(data, f, indent = '\t')

		with open('%s/%s' % (local['root'], config['checksum']), 'rb') as f:
			print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], config['checksum'], f))
			if self.do : ftp.storbinary('STOR /%s/%s' % (config['root'], config['checksum']), f)
			print('ftp.chmod(\'640\', \'/%s/%s\')' % (config['root'], config['checksum']))
			if self.do : ftp.chmod('640', '/%s/%s' % (config['root'], config['checksum']))

	def update(self, ftp, config, local, server):
		self.ensure_structure(ftp, config, local['hierarchy_tree'], server['hierarchy_tree'])
		self.update_deleted_moved_copied(ftp, config, local, server)
		self.update_added(ftp, config, local, server)
		# self.update_modified(ftp, config, local['hierarchy_tree'], server['hierarchy_tree'])
		self.update_checksum(ftp, config, local)
		self.clean_structure(ftp, config, local['hierarchy_tree'], server['hierarchy_tree'])



	def server_hash(self, ftp, config, checksum_table, hierarchy_tree, current = ''):
		for t, item in ftp.ls(current):
			print('%s%s' % (current, item))
			if item == '.' or item == '..' or item == config['checksum'] : continue
			minipath = current + item
			path = '/' + config['root'] + '/' + minipath
			if t == ftp.FILE:
				h = hashlib.sha256()
				ftp.retrbinary('RETR /%s/%s' % (config['root'], minipath), h.update)
				checksum = h.digest()
				checksum_ascii = base64.b64encode(checksum).decode('ascii')
				print(checksum_ascii)
				checksum_table.setdefault(checksum_ascii, [])
				checksum_table[checksum_ascii].append(minipath)
				hierarchy_tree[item] = checksum_ascii

			elif t == ftp.DIR:
				hierarchy_tree[item] = {}
				self.server_hash(ftp, config, checksum_table, hierarchy_tree[item], current + item + '/')

	def send_hash(self, ftp, config, data):
		with tempfile.NamedTemporaryFile('w', delete = False) as tmp:
			json.dump(data, tmp, indent = '\t')

		with open(tmp.name, 'rb') as f:
			print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], config['checksum'], f))
			ftp.storbinary('STOR /%s/%s' % (config['root'], config['checksum']), f)

		os.remove(tmp.name)

		print('ftp.chmod(\'640\', \'/%s/%s\')' % (config['root'], config['checksum']))
		ftp.chmod('640', '/%s/%s' % (config['root'], config['checksum']))
