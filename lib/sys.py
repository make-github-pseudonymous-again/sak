import functools, subprocess

def call(*args, **kwargs):
	return functools.partial(
		subprocess.Popen,
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE
	)(*args, **kwargs).communicate()