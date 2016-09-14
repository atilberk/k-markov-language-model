class LanguageModel:

	def __init__(self):
		self.table = {}

	def get(self, key):
		return self.table[key] if key in self.table else False

	def insert(self, key):
		if key not in self.table:
			self.table[key] = Markov(key)
		return self.get(key)

	def populate(self, input, preprocessor, K):
		for i in range(len(input)-K):
			key = preprocessor(input[i:i+K])
			self.insert(key).add(input[i+K])
		return self

	def printModel(self):
		print str(len(self.table))+" distinct keys"
		for key in self.table:
			print self.table[key]

	def len(self):
		return len(self.table)


from random import random, randint, choice
import string

class Markov:

	def __init__(self, substring):
		self.substring = substring
		self.frequency = 0
		self.suffixes = {}

	def add(self,suffix):
		self.frequency += 1
		self.suffixes[suffix] = (self.suffixes[suffix] if suffix in self.suffixes else 0)+1
		return self

	def random(self):
		prob = random() * self.frequency
		for suffix in self.suffixes:
			psux = self.suffixes[suffix]
			if prob < psux:
				return suffix
			prob = prob - psux
		return choice(string.ascii_letters)

	def __repr__(self):
		repr = str(str(self.frequency)+" "+self.substring+":")
		for suffix in self.suffixes:
			repr += " "+str(self.suffixes[suffix])+" "+suffix
		return repr
