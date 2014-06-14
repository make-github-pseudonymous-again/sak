import os, subprocess

def sake():
	path = os.path.join(__file__, '..', '..')
	path = os.path.abspath(path)
	subprocess.call(['git', 'pull'], cwd = path)