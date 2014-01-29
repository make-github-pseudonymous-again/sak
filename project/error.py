

class MainException(Exception):
	def __init__(self, what):
		Exception.__init__(self, what)

	def what(self):
		return self.args[0]