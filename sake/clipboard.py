import subprocess

def stdin():
	subprocess.call(["xclip", "-i", "-selection", "c"])

def stdout():
	subprocess.call(["xclip", "-o", "-selection", "c"])