import optparse
import sys

optparser = optparse.OptionParser()
optparser.add_option("-b", "--bitext", dest="bitext", default="data/dev-test-train.de-en", help="Parallel corpus (default data/dev-test-train.de-en)")
optparser.add_option("-n", "--num_sents", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
optparser.add_option("-m", "--num_words", dest="num_words", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
#optparser.add_option("-k", "--num_iterations", dest="num_iter", default=5, type="int", help="Number of iterations of the ME algorithm")
#optparser.add_option("-l", "--likelihood", dest="like", default=0, type="int", help="Print out data likelihood instead of alignments")
(opts, _) = optparser.parse_args()


def get_bitext():
	return [[sentence.strip().split() for sentence in pair.split(' ||| ')] for pair in open(opts.bitext)][:opts.num_sents]


def get_vocab():
	f_vocab = {}
	e_vocab = {}
	for (f, e) in bitext:
		for f_i in f:
			if f_i in f_vocab:
				f_vocab[f_i] += 1
			else:
				f_vocab[f_i] = 1
		for e_j in e:
			if e_j in e_vocab:
				e_vocab[e_j] += 1
			else:
				e_vocab[e_j] = 1
	vocab = {}
	vocab["E"] = e_vocab
	vocab["F"] = f_vocab
	return vocab

bitext = get_bitext()
vocab = get_vocab()
m = opts.num_words
words = sorted(vocab["E"].items(), key=lambda x: x[1])[0:m]
for (w, c) in words:
	sys.stdout.write("%s;%int\n" % (w, c))
