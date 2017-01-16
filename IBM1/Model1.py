#!/usr/bin/env python
import optparse
import sys
from collections import defaultdict
import numpy as np

optparser = optparse.OptionParser()
optparser.add_option("-b", "--bitext", dest="bitext", default="data/dev-test-train.de-en", help="Parallel corpus (default data/dev-test-train.de-en)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
optparser.add_option("-k", "--num_iterations", dest="num_iter", default=5, type="int", help="Number of iterations of the ME algorithm")
optparser.add_option("-l", "--likelihood", dest="like", default=0, type="int", help="Print out data likelihood instead of alignments")
(opts, _) = optparser.parse_args()


def get_bitext():
	return [[sentence.strip().split() for sentence in pair.split(' ||| ')] for pair in open(opts.bitext)][:opts.num_sents]


def iteration(theta):
	e_count = defaultdict(float)
	fe_count = defaultdict(float)
	for (n, (f, e)) in enumerate(bitext):
		for f_i in f:
			z = 0
			for e_j in e:
				z += theta[e_j][f_i]
			for e_j in e:
				c = theta[e_j][f_i] / z
				fe_count[(f_i, e_j)] += c
				e_count[e_j] += c
		if n % 500 == 0:
			sys.stderr.write(".")
	for (f, e) in fe_count:
		theta[e][f] = fe_count[(f, e)]/e_count[e]
	return theta


def initialize_theta():
	f_vocab = set()
	for (f, e) in bitext:
		f_vocab.update(f)
	theta = dict()
	default_p = 1.0/len(f_vocab)
	for (f, e) in bitext:
		for e_j in e:
			if not e_j in theta:
				theta[e_j] = defaultdict(float)
			for f_i in f:
				theta[e_j][f_i] = default_p
	return theta


def align(f_sent, e_sent, theta):
	a = []
	for i in range(0, len(f_sent)):
		best_prob = 0
		best_j = 0
		for j in range(0, len(e_sent)):
			if theta[e_sent[j]][f_sent[i]] > best_prob:
				best_prob = theta[e_sent[j]][f_sent[i]]
				best_j = j
		a.append((i, best_j))
	return a


def get_pair_likelihood(e_sent,f_sent,theta):
	first_column = [np.log(theta[e_j][f_sent[0]]) for e_j in e_sent]
	current_sum = list_log_add(first_column)
	for i in range(1, len(f_sent)):
		next_column = [(np.log(theta[e_j][f_sent[i]]) + current_sum) for e_j in e_sent]
		next_sum = list_log_add(next_column)
		current_sum = next_sum
	return current_sum


def list_log_add(l):
	if len(l) == 1:
		return l[0]
	else:
		new_l = []
		first_sum = log_add(l[0], l[1])
		new_l.append(first_sum)
		new_l.extend(l[2:])
		return list_log_add(new_l)


def log_add(x,y):
	# given x=ln(x') and y=ln(y') returns ln(x'+y')
	return x + np.log(1+ np.exp(y-x))


def get_data_log_likelihood(theta):
	data_log_likelihood = 0
	for (f, e) in bitext:
		data_log_likelihood += get_pair_likelihood(e,f,theta)
	return data_log_likelihood

bitext = get_bitext()
theta = initialize_theta()
k = 0

if opts.like == 1:
	while k < opts.num_iter:
		k += 1
		new_theta = iteration(theta)
		theta = new_theta
		l = get_data_log_likelihood(theta)
		sys.stderr.write("\nData log likelihood after iteration %i is %i" % (k, l))
else:
	while k < opts.num_iter:
		k += 1
		sys.stderr.write("\nTraining coefficients, iteration %i..." % k)
		new_theta = iteration(theta)
		theta = new_theta
	for (f, e) in bitext:
		a = align(f, e, theta)
		for (i, j) in a:
			sys.stdout.write("%i-%i " % (i, j))
		sys.stdout.write("\n")
	#for f in theta["ask"]:
	# 	sys.stdout.write("%s;%.15f\n" % (f, theta["asks"][f]))

