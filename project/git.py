import os, subprocess

def check(*args):
	if len(args) == 0 : args = ['.']

	for d in args:
		l = [x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))]
		if len(l) == 0 : continue
		if '.git' in l:
			out, err = subprocess.Popen(
				['git', 'status', '--porcelain'],
				cwd = d,
				stdin = subprocess.PIPE,
				stdout = subprocess.PIPE,
				stderr = subprocess.PIPE
			).communicate()
			if err != b'' : print('There\'s an error in %s' % d)
			elif out != b'' : print('There are some active changes in %s' % d)
		else : check(*[os.path.join(d, x) for x in l])