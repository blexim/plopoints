#!/usr/bin/python

import hand, features
import numpy as np
import random
import pylab
import argparse

argparser = argparse.ArgumentParser(description='Compute PLO rule sets')
argparser.add_argument('--anneal', action='store_const',
    const=True, default=False,
    help='Use simulated annealing')
argparser.add_argument('--plot', action='store_const',
    const=True, default=False,
    help='Plot graph of rules')
argparser.add_argument('--check', action='store_const',
    const=True, default=False,
    help='Check rules')
argparser.add_argument('--check_trials', type=int,
    default=1000)

argparser.add_argument('ranking', type=str,
    help='File containing hand rankings')
argparser.add_argument('hand', type=str, default=None, nargs='?',
    help='Hand to evaluate')

args = argparser.parse_args()


def read_hands(ranking_file):
  handrankings = open(ranking_file)
  hands = []
  vals = []

  for l in handrankings:
    l = l.strip()
    toks = l.split('\t')
    h = hand.Hand(toks[0])

    if len(toks) > 1:
      vals.append(int(toks[1]))

    hands.append(h)

  handrankings.close()
  
  if not vals:
    vals = range(len(hands), 0, -1)

  return (hands, vals)

def feature_names(featurelist):
  names = {}
  revnames = {}

  for feats in featurelist:
    for f in feats:
      if f not in names:
        idx = len(names)
        names[f] = idx
        revnames[idx] = f

  return (names, revnames)

def vectorize(hands):
  featurelist = [features.features(h) for h in hands]

  (names, revnames) = feature_names(featurelist)
  ret = []

  for feats in featurelist:
    row = [0] * len(names)

    for f in feats:
      idx = names[f]
      row[idx] += 1

    ret.append(row)

  return (ret, names, revnames)

def create_matrix(vectors, vals):
  A = np.vstack(vectors)
  y = np.array(vals)

  return (A, y)

def solve(A, y):
  return np.linalg.lstsq(A, y)

def normalize(soln, revnames):
  maxcoeff = max(abs(x) for x in soln)
  mincoeff = min(abs(x) for x in soln if abs(x) != 0)
  ret = {}

  for i in xrange(len(soln)):
    name = revnames[i]
    x = soln[i]

    coeff = int(x / mincoeff)
    ret[name] = coeff

  return ret

def eval(rules, hand):
  score = 0

  for feat in features.features(hand):
    score += rules[feat]

  return score

def print_rules(rules):
  for (name, coeff) in sorted(rules.items()):
    if coeff != 0:
      print "%s: %d" % (name, coeff)

def plot_rules(rules, hands, vals):
  xs = vals
  ys = [eval(rules, h) for h in hands]

  pylab.xlabel("Hand strength")
  pylab.ylabel("Score")

  pylab.plot(xs, ys, 'x')
  pylab.show()

def check(rules, hands, vals, numtrials=100000):
  correct = 0
  incorrect = 0
  total = 0

  for i in xrange(numtrials):
    idxes = random.sample(xrange(len(hands)), 2)

    idx1 = idxes[0]
    idx2 = idxes[1]

    if vals[idx1] <= vals[idx2]:
      h1 = hands[idx1]
      h2 = hands[idx2]
    else:
      h1 = hands[idx2]
      h2 = hands[idx1]

    score1 = eval(rules, h1)
    score2 = eval(rules, h2)

    if score1 <= score2:
      correct += 1
    else:
      incorrect += 1

    total += 1.0

  frac = correct / total

  return (correct, total, frac*100)

def anneal(hands, vals, maxcoeff=50, iterations=10000):
  (_, names, revnames) = vectorize(hands)
  rules = {}
  temp = maxcoeff*2
  iternum = 0
  checktrials = 1000

  for n in names:
    rules[n] = random.randint(-maxcoeff, maxcoeff)

  bestscore = 0
  best = rules

  while temp > 0:
    if iternum % (iterations / temp) == 0:
      temp = int(temp*0.8)
      print "Temperature: %d" % temp

    newrules = {}

    for n in names:
      coeff = rules[n] + random.randint(-temp, temp)
      coeff = max(coeff, -maxcoeff)
      coeff = min(coeff, maxcoeff)

      newrules[n] = coeff

    score = check(newrules, hands, vals, checktrials)[0]

    if score > bestscore:
      print "New best: %d" % score
      iternum = 0

      bestscore = score
      best = newrules

    rules = newrules
    iternum += 1

  return best

if __name__ == '__main__':
  print "Reading hand rankings..."
  (hands, vals) = read_hands(args.ranking)

  if args.anneal:
    print "Annealing..."
    rules = anneal(hands, vals)
  else:
    print "Vectorizing features..."
    (vects, names, revnames) = vectorize(hands)

    print "Created %d vectors over %d features" % (len(vects), len(names))

    print "Creating matrix..."
    (A, y) = create_matrix(vects, vals)

    print "Solving..."
    solution = solve(A, y)[0]

    rules = normalize(solution, revnames)

  print_rules(rules)

  if args.plot:
    plot_rules(rules, hands, vals)

  if args.check:
    print "Checking..."
    (correct, total, perc) = check(rules, hands, vals)

    print "%d/%d correct (%.02f%%)" % (correct, total, perc)

  if args.hand:
    h = hand.Hand(args.hand)

    print "Hand score: %d" % eval(rules, h)

  print "Done!"
