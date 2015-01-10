import lib.file, base64


def hascii(path):
	with open(path, 'rb') as f : h = lib.file.hash(f).digest()
	return base64.b64encode(h).decode('ascii')
