import lib.check, functools, subprocess, os


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


def isexecutable(fpath):
	"""http://stackoverflow.com/a/377028/1582182"""
	return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def which(program):
	"""http://stackoverflow.com/a/377028/1582182"""
	dirname = os.path.dirname(program)
	if dirname:
		if isexecutable(program) : return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):

			path = path.strip('"')
			exefile = os.path.join(path, program)

			if isexecutable(exefile) : return exefile

	return None