import lib.sys

NAVIGATOR = "google-chrome"

def open(url):
	lib.sys.call([NAVIGATOR, url]);
