from sys import stdout

class ProgressReporter():
	def __init__(self,interval=1000):
		self.counter = 0
		self.interval = interval

	def prog(self):
		self.counter += 1
		if self.counter%self.interval == 0:
			print "\rProgress: %d" % self.counter,
			stdout.flush()