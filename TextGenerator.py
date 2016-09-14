#!/usr/bin/python
import argparse, sys, re, time
from util import TimeDif, Printer
from LanguageModel import LanguageModel

def preprocessKey(key):
	return key

def getInput():
	if args.source == 'stdin':
		raw_input = sys.stdin.readlines()
	else:
		try:
			fin = open(args.source, 'r')
			raw_input = fin.read().split('\n')
			fin.close()
		except Exception, ex:
			P.rint("Error reading input from file: "+args.source, "q")
	return raw_input

def preprocessInput(raw_input):
	input = [re.sub('\s+','_',line.strip('\n')).strip() for line in raw_input]
	if args.ignore_new_line:
		input = '_'.join(input)
	else:
		input = '#'.join(input)
	return input

def postprocessOutput(raw_output):
	output = ''.join(raw_output)
	if args.ignore_new_line:
		output = re.sub('#', '_', output)
	else:
		output = re.sub('#', '\n', output)
	output = re.sub('_', ' ', output)
	return output

def writeOutput(output):
	if args.destination == "nowrite":
		return
	fout = open(args.destination, 'w')
	fout.write(output)
	fout.close()

if __name__== "__main__":

	parser = argparse.ArgumentParser(description='Text Generator for K-Markov Model')
	parser.add_argument('-K',type=int)
	parser.add_argument('-M',type=int)
	parser.add_argument('source')
	parser.add_argument('destination')
	parser.add_argument('-v', '--verbose', action='store_true')
	parser.add_argument('-q', '--quiet', action='store_true')
	parser.add_argument('-l', '--log', action='store_true')
	parser.add_argument('-i', '--ignore-new-line', action='store_true')
	args = parser.parse_args()

	if not args.K: parser.error('K value must be specified.')
	if not args.M: args.M = 0
	if args.quiet and args.verbose: parser.error("Can't run quiet and verbose at the same time.")
	if args.K < 0:
		print 'Invalid K value: K must be non-negative integer.'
		print 'Aborting...'
		exit(0)
	if args.M < 0:
		print 'Invalid M value: M must be non-negative integer.'
		print 'Aborting...'
		exit(0)

	P = Printer(args.verbose, args.quiet, args.log, "log.txt")
	P.rint("Run @ "+time.strftime('%d/%m %H:%M')+" with args: "+str(args)+"\n", "r")

	T = TimeDif()
	
	# Input variables and constants
	K = args.K
	M = args.M
	
	# read input and preprocess it
	T.start()
	input = preprocessInput(getInput())
	P.rint("Time spent for read and preprocess the input:"+str(T.dif())+"ms\n", "v")

	# initialise and populate the model
	T.start()
	LM = LanguageModel()
	LM.populate(input, preprocessKey, K);
	P.rint("Time spent for creating the language model:"+str(T.dif())+"ms\n", "v")

	# print the model if the 
	if args.verbose:
		LM.printModel()

	T.start()
	# Start by printing the first K items of the original text
	output = input[:K]
	for m in range(0, M-K):
		# take the last K items as key
		key = preprocessKey(output[-K:])
		# insert the key to the table if it doesn't exist
		# and get the next item from the model
		next = LM.insert(key).random()
		# increase the frequency of the character // edit: NO, DON'T
		#LM.get(key).add(next)
		# append the next item to the current output
		output += next
	output += '\n'

	P.rint("Time spent for generating output:"+str(T.dif())+"ms\n", "v")
	
	# print the final output with underscores replaced
	T.start()
	output = postprocessOutput(output)
	if M > 0:
		P.rint("OUTPUT:\n"+output, "r")
		writeOutput(output)
	P.rint("Time spent for preprocess and write the output:"+str(T.dif())+"ms\n", "v")
	#destruct all before close
	del(T)
	del(P)
