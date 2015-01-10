import subprocess

def timestamp():
	subprocess.call(['date', '+%s%N'])
