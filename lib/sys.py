import lib.check, functools, subprocess, os, platform


STDDEFAULT = "stddefault"

def call(cmd, *args, **kwargs):

	lib.check.SubprocessArgsEmptyException(cmd)
	lib.check.SubprocessExecutableNotFoundException(cmd[0])

	if STDDEFAULT in kwargs :
		stddefault = kwargs[STDDEFAULT]
		del kwargs[STDDEFAULT]
	else :
		stddefault = subprocess.PIPE

	popen = functools.partial(
		subprocess.Popen,
		stdin = stddefault,
		stdout = stddefault,
		stderr = stddefault
	)

	p = popen(cmd, *args, **kwargs)

	out, err = p.communicate()

	return out, err, p

def extensions():
	if platform.system() == "Windows" :
		return os.environ["PATHEXT"].split(os.pathsep)
	else :
		return [""]


def isexecutable(fpath, exts):
	"""http://stackoverflow.com/a/377028/1582182"""

	for ext in exts:
		path = fpath + ext
		if os.path.isfile(path) and os.access(path, os.X_OK) :
			return True

	return False


def which(program):
	"""http://stackoverflow.com/a/377028/1582182"""
	dirname = os.path.dirname(program)
	exts = extensions()
	if dirname:
		if isexecutable(program, exts) : return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):

			path = path.strip('"')
			exefile = os.path.join(path, program)

			if isexecutable(exefile, exts) : return exefile

	return None