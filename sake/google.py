import lib


def search(s):
	lib.sys.call(['google-chrome', "https://google.com#q=%s" % s]);