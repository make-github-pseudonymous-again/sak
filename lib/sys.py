import functools, subprocess


STDDEFAULT = "stddefault"

def call(*args, **kwargs):


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

	p = popen(*args, **kwargs)

	out, err = p.communicate()

	return out, err, p