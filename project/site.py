import ftplib, getpass, project.file, json, os, base64, tempfile, hashlib

def __ftp_is_file(ftp, path):
	if len(path) == 0 or path[0] != '/' : path = ftp.pwd() + '/' + path
	l = ftp.nlst(path)
	return len(l) == 1 and l[0] == path

def __ftp_is_dir(ftp, path):
	if len(path) == 0 or path[0] != '/' : path = ftp.pwd() + '/' + path
	l = ftp.nlst(path)
	return len(l) > 0 and l[0] != path


def __local_fetch(root, config, checksum_table, hierarchy_tree, current = '', tree = None):
	if tree == None : tree = config['tree']
	dir_list = os.listdir(root + '/' + current)
	print(dir_list)
	for item, what in tree.items():
		minipath = current + item
		path = root + '/' + minipath
		if os.path.isfile(path):
			base, ext = os.path.splitext(minipath)
			if ext == config['online_ext'] :
				if base in tree.keys() : continue
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
			__local_fetch(root, config, checksum_table, hierarchy_tree[item], current + item + '/', what)


def __server_fetch(ftp, config, server):
	checksum_file = '/%s/%s' % (config['root'], config['checksum'])
	if __ftp_is_file(ftp, checksum_file):
		chuncks = []
		ftp.retrlines('RETR %s' % checksum_file, chuncks.append)
		checksum = ''.join(chuncks)
		data = json.loads(checksum)
		server['checksum_table'] = data['checksum_table']
		server['hierarchy_tree'] = data['hierarchy_tree']

	print(json.dumps(server['checksum_table'], indent = '\t'))
	print(json.dumps(server['hierarchy_tree'], indent = '\t'))


def __update_deleted_moved_copied(ftp, config, local, server):
	for checksum, minipaths in server['checksum_table'].items():

		# deleted files
		if checksum not in local['checksum_table']:
			for i in range(len(minipaths)):
				print('ftp.delete(\'/%s/%s\')' % (config['root'], minipaths[i]))
				# ftp.delete('/%s/%s' % (config['root'], minipaths[i]))

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
						# ftp.rename('/%s/%s' % (config['root'], minipath), '/%s/%s' % (config['root'], replace))
					else:
						print('ftp.delete(\'/%s/%s\')' % (config['root'], minipath))
						# ftp.delete('/%s/%s' % (config['root'], minipath)

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
						# ftp.storbinary('STOR /%s/%s' % (config['root'], not_handled[i]), f)


def __update_added(ftp, config, local, server):
	for checksum, paths in local['checksum_table'].items():
		# added files
		if checksum not in server['checksum_table']:
			for i in range(len(paths['s'])):
				with open('%s/%s' % (local['root'], paths['s'][i]), 'rb') as f:
					print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], paths['d'][i], f))
					# ftp.storbinary('STOR /%s/%s' % (config['root'], paths[i]['d']), f)

def __update_modified(ftp, config, local_h, server_h, current = ''):

	for item, data in local_h.items():
		# modified files
		if type(data) == list:
			checksum, dest = data
			if dest in server_h and checksum != server_h[dest]:
				with open('%s/%s%s' % (local['root'], current, item), 'rb') as f:
					print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], current, dest, f))
					# ftp.storbinary('STOR /%s/%s' % (config['root'], minipath), f)


		elif item in server_h:
			__update_modified(ftp, config, data, server_h[item], current + item + '/')


def __update_checksum(ftp, config, local):
	data = {
		'checksum_table' : {},
		'hierarchy_tree' : {}
	}

	for key in local['checksum_table']:
		data['checksum_table'][key] = local['checksum_table'][key]['d']

	with open('%s/%s' % (local['root'], config['checksum']), 'w') as f:
		json.dump(data, f, indent = '\t')

	with open('%s/%s' % (local['root'], config['checksum']), 'rb') as f:
		print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], config['checksum'], f))
		# ftp.storbinary('STOR /%s/%s' % (config['root'], config['checksum']), f)
		print('ftp.sendcmd(\'SITE CHMOD 640 /%s/%s\')' % (config['root'], config['checksum']))
		# ftp.sendcmd('SITE CHMOD 640 /%s/%s' % (config['root'], config['checksum']))

def __update(ftp, config, local, server):
	__update_deleted_moved_copied(ftp, config, local, server)
	__update_added(ftp, config, local, server)
	# __update_modified(ftp, config, local['hierarchy_tree'], server['hierarchy_tree'])
	__update_checksum(ftp, config, local)


def __ftp_login(config):

	ftp = ftplib.FTP()
	print(ftp.connect(config['host']))
	username = config['username'] if 'username' in config else input('Username for \'ftp://%s\' : ' % (config['host']))
	password = getpass.getpass('Password for \'ftp://%s@%s\' : ' % (username, config['host']))
	print(ftp.login(username, password))
	print(ftp.cwd(config['root']))

	return ftp

def up(directory, config_file):

	local = {
		'root' : os.path.abspath(directory),
		'checksum_table' : {},
		'hierarchy_tree' : {}
	}

	# fetch the config file to upload
	with open(config_file, 'r') as f:
		config = json.load(f)

	# build the local tree and table
	__local_fetch(local['root'], config, local['checksum_table'], local['hierarchy_tree'])

	print(json.dumps(local['checksum_table'], indent = '\t'))
	print(json.dumps(local['hierarchy_tree'], indent = '\t'))

	try:

		ftp = __ftp_login(config)

		server = {
			'root' : config['root'],
			'checksum_table' : {},
			'hierarchy_tree' : {}
		}

		# fetch the server tree and table
		__server_fetch(ftp, config, server)

		# try to patch server by analyzing (diff local server)
		__update(ftp, config, local, server)

	# except ftplib.all_errors as e:
	# 	print('Socket error : %s' % (e))

	finally:
		ftp.quit()

# FTP.rename(fromname, toname)
# FTP.delete(filename)
# FTP.mkd(pathname)
# FTP.rmd(dirname)



def __server_hash(ftp, config, checksum_table, hierarchy_tree, current = ''):
	for item in ftp.nlst(current):
		print('%s%s' % (current, item))
		if item == '.' or item == '..' or item == config['checksum'] : continue
		minipath = current + item
		path = '/' + config['root'] + '/' + minipath
		if __ftp_is_file(ftp, path):
			h = hashlib.sha256()
			ftp.retrbinary('RETR /%s/%s' % (config['root'], minipath), h.update)
			checksum = h.digest()
			checksum_ascii = base64.b64encode(checksum).decode('ascii')
			print(checksum_ascii)
			checksum_table.setdefault(checksum_ascii, [])
			checksum_table[checksum_ascii].append(minipath)
			# hierarchy_tree[item] = checksum_ascii

		elif __ftp_is_dir(ftp, path):
			# hierarchy_tree[item] = {}
			__server_hash(ftp, config, checksum_table, hierarchy_tree, current + item + '/') # hierarchy_tree[item]

def __send_hash(ftp, config, data):
	with tempfile.NamedTemporaryFile('w', delete = False) as tmp:
		json.dump(data, tmp, indent = '\t')

	with open(tmp.name, 'rb') as f:
		print('ftp.storbinary(\'STOR /%s/%s\', %s)' % (config['root'], config['checksum'], f))
		ftp.storbinary('STOR /%s/%s' % (config['root'], config['checksum']), f)

	os.remove(tmp.name)

	print('ftp.sendcmd(\'SITE CHMOD 640 /%s/%s\')' % (config['root'], config['checksum']))
	ftp.sendcmd('SITE CHMOD 640 /%s/%s' % (config['root'], config['checksum']))


def hash(config_file):

	# fetch the config file to upload
	with open(config_file, 'r') as f:
		config = json.load(f)

	try:

		ftp = __ftp_login(config)

		server = {
			'checksum_table' : {},
			'hierarchy_tree' : {}
		}

		# build the server tree and table
		__server_hash(ftp, config, server['checksum_table'], server['hierarchy_tree'])

		# send it
		__send_hash(ftp, config, server)

	# except ftplib.all_errors as e:
	# 	print('Socket error : %s' % (e))

	finally:
		ftp.quit()