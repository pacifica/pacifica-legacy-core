class jsonentry:
	def __init__(self, entry, strentry=None):
		self.entry = entry
		self.strentry = None
		self.done_cb = []
	def done(self, is_ok):
		for i in self.done_cb:
			i(self, is_ok)

