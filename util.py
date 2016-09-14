class Printer:
	def __init__(self,v,q,l,ldest):
		self.v = v
		self.q = q
		self.l = l
		self.f = open(ldest, 'a') if l else None

	def rint(self,message,cond):
		if self.l and self.f is not None:
			self.f.write(message)

		if cond is "v":
			if not self.v:
				return
		elif cond is "r":
			if self.q:
				return
		elif cond is "q":
			pass
		print message,

	def _del_(self):
		self.f.close()


from datetime import datetime

class TimeDif:
	def __init__(self):
		self.start_time = None

	def start(self):
		self.start_time = datetime.now()
		return self

	def how(self):
		return datetime.now()

	def dif(self):
		return int((self.how() - self.start_time).total_seconds() * 1000)